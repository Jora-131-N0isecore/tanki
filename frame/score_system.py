class ScoreSystem:
    def __init__(self, filename="records.txt"):
        self.filename = filename
        self.current_score = 0
        self.current_level = 1
        self.records = {}
        self.load_records()

    def load_records(self):
        #Загружает рекорды из файла
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        level, score = line.split(':')
                        self.records[int(level)] = int(score)
        except FileNotFoundError:
            self.records = {}

    def save_records(self):
        #Сохраняет рекорды в файл
        with open(self.filename, 'w', encoding='utf-8') as f:
            for level, score in self.records.items():
                f.write(f"{level}:{score}\n")

    def set_level(self, level):
        self.current_level = level

    def add_points(self, points):
        self.current_score += points

    def check_and_save_record(self):
        #Проверяет и сохраняет рекорд для текущего уровня
        if self.current_level not in self.records or self.current_score > self.records[self.current_level]:
            self.records[self.current_level] = self.current_score
            self.save_records()
            return True
        return False

    def get_record_for_level(self, level):
        return self.records.get(level, 0)

    def get_current_score(self):
        return self.current_score

    def reset_current_score(self):
        self.current_score = 0