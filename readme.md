# DDP App

<!--- mdtoc: toc begin -->

1.	[Installation](#installation)
2.	[Configuration](#configuration)
3.	[Usage](#usage)<!--- mdtoc: toc end -->

## Installation

1.	Make sure python yaml module is installed

	```python
	pip install pyyaml
	```

2.	Edit `local.py` to make sure that app gets imported.

	```python
	sys.path.append('/home/rdmo/ddp-app')
	INSTALLED_APPS += [
	    'ddpapp'
	]
	```

## Configuration

The configuration file is in the `ddp-app` folder. Edit `conf.yaml`

## Usage

Load the tags in your view and use them.

```
{% load ddp_view_tags %}
```
