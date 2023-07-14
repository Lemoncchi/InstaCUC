# InstaCUC

## 简介

> 本项目基于教程 [Flask Web 开发实战](https://helloflask.com/book/1/) 和开源项目 [InstaCUC](https://github.com/greyli/instacuc) 二次开发而成

### 特色

- 基于 `Flask` 框架
- `unittest` 单元测试

## Installation

clone:

```
$ git clone https://github.com/greyli/instacuc.git
$ cd instacuc
```

### virtualenv 安装:

```
$ python -m venv env
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```

### Pipenv 安装:

```
$ pipenv install --dev
$ pipenv shell
```

generate fake data then run:

```
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
