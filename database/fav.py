import csv

class Favorites():

    def __init__(self):
        self.favs = set()
        with open("resources/data/fav.csv") as fav_file:
            csv_reader = csv.reader(fav_file)
            for row in csv_reader:
                try:
                    self.favs = self.favs.union(set([int(row[0])]))
                except:
                    pass

    def __iter__(self):
        return iter(self.favs)

    def append(self, key):
        self.favs = self.favs.union({key})
        with open("resources/data/fav.csv", "w", newline='') as fav_file:
            csv_writer = csv.writer(fav_file)
            for item in self.favs:
                csv_writer.writerow([item])

    def remove(self, key):
        self.favs = self.favs.difference({key})
        with open("resources/data/fav.csv", "w") as fav_file:
            csv_writer = csv.writer(fav_file)
            for item in self.favs:
                csv_writer.writerow([item])
