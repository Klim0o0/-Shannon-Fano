# Shannon-Fano


##Установка
Для работы требуется bitarray
```
    pip install bitarray
```

##Запуск
Архивация
```
    python -m compress file/dir
    python -m compress arcive_name [files/dirs]
```

Разархивация
```
    python -m decompress arcive target_path
    python -m decompress arcive target_path [files_for_decompress]
    ключ -i игнорирвать ошибки в файлах
```

Получить список файлов в архиве
```
    python -m get arcive
```