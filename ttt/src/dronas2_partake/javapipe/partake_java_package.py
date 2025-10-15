import os

from aslogic_java_bundles.main_java_package import MAIN_JAVA_BUNDLE
from javapipe.java_bundle import UserJavaPackage, UserJavaBundle

PARTAKE_JAVA_BUNDLE = UserJavaBundle(
    'dronas',
    os.path.dirname(os.path.abspath(__file__)) + '/pom.xml',
    os.path.dirname(os.path.abspath(__file__)) + "/../../../javalib",
    os.path.dirname(os.path.abspath(__file__)) + "/../../../pyi",
    user_packages=[
        UserJavaPackage('es.aslogic.partake', 'uab-snapshots'),
        UserJavaPackage('es.aslogic.geom', 'uab-snapshots')
    ],
    dependencies=[MAIN_JAVA_BUNDLE]
)
