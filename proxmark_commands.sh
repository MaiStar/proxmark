#!/bin/bash

# Запуск
#./proxmark_commands.sh

# Путь к файлу для сохранения результатов
output_file=~/Python/proxmark/output.txt

# Очищаем содержимое файла перед началом
> $output_file

# Очищаем карту перед началом
./pm3 -c "hf mf wrbl --blk 8 -k 59D7FD628402 -d 00000000000000000000000000000000"

# Цикл 200 50 2000
# Цикл 1700 5 1750
for delay in $(seq 200 50 2000); do
  # Получаем текущее время в формате ЧЧ:ММ:СС
  current_time=$(date +"%H:%M:%S")
  
  # Пишем задержку и текущее время в файл
  echo "$delay" >> $output_file
  echo "$current_time" >> $output_file
  
  # Выполняем команду и записываем результат 10 раз / ~ 24 минуты
  # Выполняем команду и записываем результат 50 раз / ~ 37 минут
  # for i in {1..10}; do 
  # for i in {1..50}; do 
  for i in {1..10}; do 
    # Выполняем команду hw tearoff с текущей задержкой
    ./pm3 -c "hw tearoff --delay $delay --on"
    
    # Пишем в карту
    ./pm3 -c "hf mf wrbl --blk 8 -k 59D7FD628402 -d 000102030405060708090a0b0c0d0e0f"
    
    # Выполняем команду hf mf rdsc и фильтруем нужную строку
    result=$(./pm3 -c "hf mf rdsc -s 2 -k 59D7FD628402" | grep "  8 |")
    
    # Очищаем карту ещё раз
    ./pm3 -c "hf mf wrbl --blk 8 -k 59D7FD628402 -d 00000000000000000000000000000000"
    
    # Записываем результат в файл
    echo "$result" >> $output_file
  done
done

echo -e "\a"
