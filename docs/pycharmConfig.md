### 1) Set up docker python interpreter for pycharm
```
1.1) go to 
	→ settings 
	→ Project 
	→ Project Interpreter
	→ click in the gear button (up right corner)
	→ show all
	→ add (button)
	→ Docker Compose
```
```
1.2) Configuration steps
	→ new Docker Server (if not one already exist)
	→ Configuration file(s) : ./docker-compose.yml
	→ Service : wayne-app
	→ click ok 
```
### 2) Configure Django Server
```
2.1) go to 
	→ Run 
	→ Edit Configuration
```
```
2.2) Configuration steps
	→ create a Django Server (if not one already exist)
	→ Host : 0.0.0.0
	→ Port : 8000
	→ add variable DJANGO_SETTINGS_MODULE=wayne.settings
	→ Python interpreter : choose the remote interpreter that you created before 
	→ Working directory : /data/www
```

### 3) If you want to enable the debugger
```
3.1) go to 
	→ Run 
	→ Edit Configuration
	→ Django server you created before
```
```
3.2) Configuration steps
	→ check the “No reload” checkbox

```
### ![#f03c15](https://placehold.it/15/f03c15/000000?text=+) Attention
Keep in mind that if you enable the No reload checkbox, you have to reload your application whenever you change your code.
