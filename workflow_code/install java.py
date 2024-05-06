import jdk
jdk.install('11', impl=jdk.Implementation.OPENJ9)

import os
jdk_version = 'jdk-11.0.19+7'  # Change this to your desired version
os.environ['JAVA_HOME'] = f'/root/.jdk/{jdk_version}'
os.environ['PATH'] = f"{os.environ.get('PATH')}:{os.environ.get('JAVA_HOME')}/bin"
