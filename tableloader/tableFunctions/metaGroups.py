import sys
import os
from sqlalchemy import Table
from yaml import load

try:
    from yaml import CSafeLoader as SafeLoader
    print("Using CSafeLoader")
except ImportError:
    from yaml import SafeLoader
    print("Using Python SafeLoader")


def importyaml(connection, metadata, source_path, language='en'):
    print("Importing metaGroups")
    invMetaGroups = Table('invMetaGroups', metadata)
    trnTranslations = Table('trnTranslations', metadata)

    print("opening Yaml")
    trans = connection.begin()

    with open(
        os.path.join(source_path, 'fsd', 'metaGroups.yaml'), 'r'
    ) as yamlstream:
        print("importing")
        metagroups = load(yamlstream, Loader=SafeLoader)
        print("Yaml Processed into memory")
        for metagroupid in metagroups:
            connection.execute(
                invMetaGroups.insert(),
                metaGroupID=metagroupid,
                metaGroupName=metagroups[metagroupid].get('nameID', {}).get(language, ''),
                iconID=metagroups[metagroupid].get('iconID'),
                description=metagroups[metagroupid].get('descriptionID', {}).get(language, '')
            )

            if 'nameID' in metagroups[metagroupid]:
                for lang in metagroups[metagroupid]['nameID']:
                    try:
                        connection.execute(
                            trnTranslations.insert(),
                            tcID=34,
                            keyID=metagroupid,
                            languageID=lang,
                            text=metagroups[metagroupid]['nameID'][lang]
                        )
                    except:
                        print('{} {} has a category problem'.format(metagroupid, lang))
            if 'descriptionID' in metagroups[metagroupid]:
                for lang in metagroups[metagroupid]['descriptionID']:
                    try:
                        connection.execute(
                            trnTranslations.insert(),
                            tcID=35,
                            keyID=metagroupid,
                            languageID=lang,
                            text=metagroups[metagroupid]['descriptionID'][lang]
                        )
                    except:
                        print('{} {} has a category problem'.format(metagroupid, lang))
    trans.commit()
