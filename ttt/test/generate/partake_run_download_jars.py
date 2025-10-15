import logging
import os

from dronas2_partake.javapipe.partake_java_package import PARTAKE_JAVA_BUNDLE
from javapipe.java_bundle import JavapipeGenerator
from javapipe.javadocreader import PrivateMavenJavadocParser, PublicMavenJavadocParser


def main():

    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    generator = JavapipeGenerator([PARTAKE_JAVA_BUNDLE])

    if not generator.download(logger):
        return False

    if not generator.explore(logger):
        return False

    if not generator.javadocs({
        'java-base': PublicMavenJavadocParser(
            'https://docs.oracle.com/en/java/javase/21/docs/api/java.base/module-summary.html'
        ),
        'uab-snapshots': PrivateMavenJavadocParser(
            'https://uspace.uab.es/mvn/javadoc/snapshots/',
            'server',
            'RRCR1kMkfzKxd/uhlihlYuwQrNM5gb0X4ssSRV9Q8q3yQABY/vblbLbzU1PCGnQR',
            cache=os.path.dirname(os.path.abspath(__file__)) + "/../../cache/",
        ),
        'uab-releases': PrivateMavenJavadocParser(
            'https://uspace.uab.es/mvn/javadoc/releases/',
            'server',
            'RRCR1kMkfzKxd/uhlihlYuwQrNM5gb0X4ssSRV9Q8q3yQABY/vblbLbzU1PCGnQR',
            cache=os.path.dirname(os.path.abspath(__file__)) + "/../../cache/",
        )
    }):
        return False

    if not generator.generate_stubs(logger):
        return False

    return True

if __name__ == '__main__':
    main()
