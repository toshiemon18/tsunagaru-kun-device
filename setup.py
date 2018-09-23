from setuptools import setup
from setuptools import find_packages

long_description = '''
つながるくんデバイス用ソフトウェア
ハードウェア構成
    - RaspberryPi Zero W v1.1
        - OS: Raspbian Stretch Lite
    - ADS1015
        - VDD -> PIN 1
        - GND -> PIN 6
        - SCL -> PIN 5
        - SDA -> PIN 3
    - CT sensor 3702-150N
        - 負荷抵抗 100[ohm]
        - l(K) -> ADS1015 A0 PIN
        - k(L) -> ADS1015 GND PIN
'''

setup(name='tsunagaru-kun-device',
      version='0.1.0',
      description='つながるくんデバイス用ソフトウェア',
      long_description=long_description,
      author='Francois Chollet',
      author_email='st17807@tomakomai.kosen-ac.jp',
      url='https://github.com/toshiemon18',
      download_url='https://github.com/toshiemon18/tsunagaru-kun-device',
      license='MIT',
      install_requires=[
          'adafruit-ads1x15',
          'numpy'
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=find_packages())
