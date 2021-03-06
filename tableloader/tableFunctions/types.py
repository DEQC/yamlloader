import os
from yaml import load, dump
from utils import yaml_stream
from sqlalchemy import Table

try:
    from yaml import CSafeLoader as SafeLoader
    print ("Using CSafeLoader")
except ImportError:
    from yaml import SafeLoader
    print ("Using Python SafeLoader")


def importyaml(connection, metadata, source_path, language='en'):
    invTypes = Table('invTypes', metadata)
    trnTranslations = Table('trnTranslations', metadata)
    certMasteries = Table('certMasteries', metadata)
    invTraits = Table('invTraits', metadata)
    invMetaTypes = Table('invMetaTypes', metadata)

    print("Importing Types")
    print("Opening Yaml")

    with open(
        os.path.join(source_path, 'fsd', 'typeIDs.yaml'), 'r'
    ) as yamlstream:
        trans = connection.begin()
        typeids = load(yamlstream, Loader=SafeLoader)
        print("Yaml Processed into memory")
        for typeid in typeids:
            connection.execute(
                invTypes.insert(),
                typeID=typeid,
                groupID=typeids[typeid].get('groupID', 0),
                typeName=typeids[typeid].get('name', {}).get(language, ''),
                description=typeids[typeid].get('description', {}).get(language, ''),
                mass=typeids[typeid].get('mass', 0),
                volume=typeids[typeid].get('volume', 0),
                capacity=typeids[typeid].get('capacity', 0),
                portionSize=typeids[typeid].get('portionSize'),
                raceID=typeids[typeid].get('raceID'),
                basePrice=typeids[typeid].get('basePrice'),
                published=typeids[typeid].get('published', 0),
                marketGroupID=typeids[typeid].get('marketGroupID'),
                graphicID=typeids[typeid].get('graphicID', 0),
                iconID=typeids[typeid].get('iconID'),
                soundID=typeids[typeid].get('soundID')
            )
            if "masteries" in typeids[typeid]:
                for level in typeids[typeid]["masteries"]:
                    for cert in typeids[typeid]["masteries"][level]:
                        connection.execute(
                            certMasteries.insert(),
                            typeID=typeid,
                            masteryLevel=level,
                            certID=cert
                        )
            if 'name' in typeids[typeid]:
                for lang in typeids[typeid]['name']:
                    connection.execute(
                        trnTranslations.insert(),
                        tcID=8,
                        keyID=typeid,
                        languageID=lang,
                        text=typeids[typeid]['name'][lang]
                    )
            if 'description' in typeids[typeid]:
                for lang in typeids[typeid]['description']:
                    connection.execute(
                        trnTranslations.insert(),
                        tcID=33,
                        keyID=typeid,
                        languageID=lang,
                        text=typeids[typeid]['description'][lang]
                    )
            if 'traits' in typeids[typeid]:
                if 'types' in typeids[typeid]['traits']:
                    for skill in typeids[typeid]['traits']['types']:
                        for trait in typeids[typeid]['traits']['types'][skill]:
                            result = connection.execute(
                                invTraits.insert(),
                                typeID=typeid,
                                skillID=skill,
                                bonus=trait.get('bonus'),
                                bonusText=trait.get('bonusText', {}).get(language, ''),
                                unitID=trait.get('unitID')
                            )
                            traitid = result.inserted_primary_key
                            for languageid in trait.get('bonusText',{}):
                                connection.execute(
                                    trnTranslations.insert(),
                                    tcID=1002,
                                    keyID=traitid[0],
                                    languageID=languageid,
                                    text=trait['bonusText'][languageid]
                                )
                if 'roleBonuses' in typeids[typeid]['traits']:
                    for trait in typeids[typeid]['traits']['roleBonuses']:
                        result = connection.execute(
                            invTraits.insert(),
                            typeID=typeid,
                            skillID=-1,
                            bonus=trait.get('bonus'),
                            bonusText=trait.get('bonusText', {}).get(language, ''),
                            unitID=trait.get('unitID')
                        )
                        traitid = result.inserted_primary_key
                        for languageid in trait.get('bonusText', {}):
                            connection.execute(
                                trnTranslations.insert(),
                                tcID=1002,
                                keyID=traitid[0],
                                languageID=languageid,
                                text=trait['bonusText'][languageid]
                            )
                if 'miscBonuses' in typeids[typeid]['traits']:
                    for trait in typeids[typeid]['traits']['miscBonuses']:
                        result = connection.execute(
                            invTraits.insert(),
                            typeID=typeid,
                            skillID=-2,
                            bonus=trait.get('bonus'),
                            bonusText=trait.get('bonusText',{}).get(language,''),
                            unitID=trait.get('unitID')
                        )
                        traitid=result.inserted_primary_key
                        for languageid in trait.get('bonusText', {}):
                            connection.execute(
                                trnTranslations.insert(),
                                tcID=1002,
                                keyID=traitid[0],
                                languageID=languageid,
                                text=trait['bonusText'][languageid]
                            )
            if 'metaGroupID' in typeids[typeid] or 'variationParentTypeID' in typeids[typeid]:
                connection.execute(
                    invMetaTypes.insert(),
                    typeID=typeid,
                    metaGroupID=typeids[typeid].get('metaGroupID'),
                    parentTypeID=typeids[typeid].get('variationParentTypeID')
                )
    trans.commit()
