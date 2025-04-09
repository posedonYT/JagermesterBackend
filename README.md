# Jagermester Kombat api

```PYTHON
if __name__ == "__main__":
    api_process = multiprocessing.Process(target=run_api)
    bot_process = multiprocessing.Process(target=bot_process_func)

    api_process.start()
    bot_process.start()

    api_process.join()
    bot_process.join()
   ```

### Ссылка на frontend 
```
https://jugermester-kombat.vercel.app/
```