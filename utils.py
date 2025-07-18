fiyatlar = {
    "corba": 20,
    "sulu": 50,
    "izgara": 70,
    "tatli": 30,
    "salata": 15,
    "icecek": 5,
    "kuru": 20
}

def fiyat_hesapla(etiket):
    return fiyatlar.get(etiket, 0)
