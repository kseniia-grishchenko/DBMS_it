import Pyro5.api


uri = input("Pyro uri of Db Manager: ").strip()

db_manager = Pyro5.api.Proxy(uri)
# db_manager.create_database("test_pyro")
db_manager.open_database("test_pyro")

db_manager.add_table("pyro")

Pyro5.api.Proxy(db_manager.get_table("pyro"))

db_manager.save_database("test_pyro")
