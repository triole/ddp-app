## DDP App

<!--- mdtoc: toc begin -->

1.	[DDP App](#ddp-app)<!--- mdtoc: toc end -->

# How to install?

Edit `local.py` to make sure that app gets imported.

```python
sys.path.append('/home/rdmo/ddp-app')
INSTALLED_APPS += [
    'ddp-app'
]
```
