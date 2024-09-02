#!/bin/bash

# Запуск
#./proxmark_commands.sh

# Путь к файлу для сохранения результатов
output_file=~/Музыка/output.txt

# Очищаем содержимое файла перед началом
> $output_file

# Очищаем карту началом
./pm3 -c "hf mf wrbl --blk 8 -k 59D7FD628402 -d 00000000000000000000000000000000"

# Цикл от 200 до 2000 с шагом 50
for delay in $(seq 1700 10 1700); do
#for delay in $(seq 200 50 2000); do
  # Пишем задержку в файл
  echo "$delay" >> $output_file
  
  # Выполняем команду и записываем результат 10 раз
  for i in {1..40}; do
    # Выполняем команду hw tearoff с текущей задержкой
    ./pm3 -c "hw tearoff --delay $delay --on"
    
    # Пишем в карту
    ./pm3 -c "hf mf wrbl --blk 8 -k 59D7FD628402 -d 000102030405060708090a0b0c0d0e0f"
    
    # Выполняем команду hf mf rdsc и фильтруем нужную строку
    result=$(./pm3 -c "hf mf rdsc -s 2 -k 59D7FD628402" | grep "  8 |")
    
    # Записываем результат в файл
    echo "$result" >> $output_file
  done
done

