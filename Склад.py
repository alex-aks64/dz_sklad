from threading import Thread, Lock
import multiprocessing as mp

lock = Lock()
requests = [
    ("product1", "receipt", 100),
    ("product2", "receipt", 150),
    ("product1", "shipment", 30),
    ("product3", "receipt", 200),
    ("product2", "shipment", 50)
]


class WarehouseManager:
    def __init__(self):
        self.data = {}

    def process_request(self, request, s_dict, lock):
        lock.acquire()
        try:
            product, operation, amount = request
            if operation == "receipt":
                if product in s_dict:
                    s_dict[product] += amount
                else:
                    s_dict[product] = amount
            elif operation == "shipment":
                if product in s_dict and s_dict[product] >= amount:
                    s_dict[product] -= amount
                else:
                    print("Нет товаров для выдачи")

        finally:
            lock.release()

    def run(self, requests):
        s_dict = mp.Manager().dict()
        lock = mp.Lock()
        processes = [mp.Process(target=self.process_request, args=(req, s_dict, lock)) for req in requests]

        for p in processes:
            p.start()
        for p in processes:
            p.join()
        self.data = dict(s_dict)



if __name__ == "__main__":
    manager = WarehouseManager()
    manager.run(requests)
    print(manager.data)
