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

