# IS309 Course Project: Experiments on Textbook RSA

## 1. Task 1：实现 *textbook RSA*

- 生成指定 *size* 的密钥：

    ```shell
    python textbook_RSA.py --generate_keys --key_size 1024 
    ```

- 加密指定路径的 *plaintext* 文件（ `txt` 格式）：

    ```shell
    python textbook_RSA.py --encrypt_file ./test/plaintext.txt 
    ```

- 解密指定路径的 *ciphertext* 文件（ `txt` 格式）：

    ```shell
    python textbook_RSA.py --decrypt_file ./test/ciphertext.txt
    ```

-----



## 2. Task 2: 基于 *textbook RSA* 实现 *CCA2 attack*

- 若需要更新 *client* 和 *server* 之间的 *RSA* 密钥，请参考 *task 1* 中重新生成指定 *size* 的密钥

- 指定 *AES key* 的大小，模拟在 *client* 和 *server* 之间的 *CCA2 attack*：

    ```shell
    python CCA2_attack.py --key_size 128
    ```

    

    
