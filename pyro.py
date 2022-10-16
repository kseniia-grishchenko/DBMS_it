import Pyro5.api


uri = "PYRO:obj_ae7b5371248d4520b43df4ece71030af@localhost:49849"

name = input("Enter db name:\n").strip()
db_manager = Pyro5.api.Proxy(uri)
Pyro5.api.Proxy(db_manager.create_database("test_2"))
