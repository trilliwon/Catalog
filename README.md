# Movie Catalog

> This application provides a movie catalog, the categories will be given and authorized user can add, edit or delete their items.
> User can be authorized by google account.

---

## Requirements

- `Python 3.7.1`
- `Vagrant 2.2.4`
- `VirtualBox 6.0.6`
- `oauth2client 4.1.3`
- `Flask 1.0.2`
- `SQLAlchemy-1.3.3`

> To setup environment, follow the instruction [here](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

---

## How to run the application

### macOS (Prefered)

1. `git clone https://github.com/trilliwon/Catalog.git`
2. `cd Catalog/vagrant/catalog`
3. `python3 database_setup.py`
4. `python3 create_sample_data.py`
5. `python3 app.py`
6. `open http://localhost:5000`

### Virtualbox

1. `git clone https://github.com/trilliwon/Catalog.git`
2. `cd Catalog/vagrant`
3. `vagrant up`
4. `vagrant ssh`
5. `cd /vagrant/catalog`
6. `python3 database_setup.py`
7. `python3 create_sample_data.py`
8. `python3 app.py`

#### Important
> When using vagrant, there's a problem with connect `localhost:5000` from browser. With host `0.0.0.0:5000`, I am able to access from browser. But in this case, **I could not able to login to google**.



## Screenshots


### User points

### Login

<img width="1440" alt="login" src="https://user-images.githubusercontent.com/14218787/57578194-7a8c4000-74c2-11e9-9895-abe010fdbedb.png">

---

### Main (logged in user)

<img width="1440" alt="loggedinuser" src="https://user-images.githubusercontent.com/14218787/57578195-7b24d680-74c2-11e9-993c-c02569f8b622.png">

---

### Add Item

<img width="1440" alt="additem" src="https://user-images.githubusercontent.com/14218787/57578196-7b24d680-74c2-11e9-8f43-856d50ca2c60.png">

---

### Delete Item
<img width="1440" alt="deleteitem" src="https://user-images.githubusercontent.com/14218787/57578197-7b24d680-74c2-11e9-9d8e-3b0624d6e7e9.png">

---

### Editing 

<img width="1440" alt="editing" src="https://user-images.githubusercontent.com/14218787/57578198-7b24d680-74c2-11e9-89e3-9f9f3e0439c0.png">

---

### Read Item

<img width="1439" alt="loggedindetail" src="https://user-images.githubusercontent.com/14218787/57578199-7bbd6d00-74c2-11e9-9041-78007c5d737b.png">

---

### Main (logged in)

<img width="1440" alt="main" src="https://user-images.githubusercontent.com/14218787/57578200-7bbd6d00-74c2-11e9-9daa-2f834b7164bc.png">

---

### Main
<img width="1439" alt="notloggedin" src="https://user-images.githubusercontent.com/14218787/57578201-7c560380-74c2-11e9-916d-a60b1134bfff.png">

---

### JSON Endpoints

- http://localhost:5000/category/horror/item/10/JSON

```
{
  "CategoryItem": {
    "category": "HORROR", 
    "description": "An anthology series that tells startling, stranger-than-fiction true crime stories, including a girl trying to escape her overprotective and abusive mother.", 
    "id": 10, 
    "name": "The Act"
  }
}
```

- http://localhost:5000/category/comedy/items/JSON

```
{
  "CategoryItems": [
    {
      "category": "COMEDY", 
      "description": "Following the events of Avengers: Endgame, Spider-Man must step up to take on new threats in a world that has changed forever.", 
      "id": 1, 
      "name": "Spider-Man: Far from Home"
    }, 
    {
      "category": "COMEDY", 
      "description": "In a world where people collect Pok\u00e9mon to do battle, a boy comes across an intelligent talking Pikachu who seeks to be a detective.", 
      "id": 2, 
      "name": "Pok\u00e9mon Detective Pikachu"
    }, 
    {
      "category": "COMEDY", 
      "description": "A kindhearted street urchin and a power-hungry Grand Vizier vie for a magic lamp that has the power to make their deepest wishes come true.", 
      "id": 3, 
      "name": "Aladdin"
    }, 
    {
      "category": "COMEDY", 
      "description": "Thor is imprisoned on the planet Sakaar, and must race against time to return to Asgard and stop Ragnar\u00f6k, the destruction of his world, at the hands of the powerful and ruthless villain Hela.", 
      "id": 4, 
      "name": "Thor: Ragnarok"
    }
  ]
}
```


## Developer

- @trilliwon