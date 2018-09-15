# つながるくんデバイス for RaspberryPi

## installation
- Python3のみサポート
### Pythonのインストール
```
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
$ exec $SHELL -l
$ pyenv install 3.6.2
```
echoコマンドのリダイレクト先は仕様しているシェルに合わせて読み替えて.
インストールするバージョンは3系であれば何でも良い.


### 本体のインストール
```
$ git clone https://github.com/toshiemon18/tsunagaru-kun-device.git
$ python setup.py
```
