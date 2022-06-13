from pathlib import Path


ID = Path('./input.txt').read_text().splitlines()[0]
TOKEN = Path('./input.txt').read_text().splitlines()[1]

MESSAGE = 'Девушка дня'

main_word = 'девушка'
kind = 'бодибилдинг бодифитнес фитнес-модель фитнес-бикини'.split(' ')
keywords = ('сексуальные любительские горячие чемпионка модель позирует '
            + 'мускулистая загорелая соревнования '
            + 'бикини пляж вода бассейн зал тренажер тренировка '
            + 'ринг дома селфи атлетичная фото лето море').split(' ')

main_word2 = 'female'
kind2 = 'bodybuilding bodyfitness fitness-model fitness-bikini'.split(' ')
keywords2 = ('sexy amateur hot champion model pose '
            + 'muscle sun-tanned contest competition '
            + 'bikini beach water pool gym training  '
            + 'ring home selfie outdoors workout photo '
            + 'summer sea').split(' ')

REQUEST_PARAMS = ((main_word, kind, keywords), (main_word2, kind2, keywords2))