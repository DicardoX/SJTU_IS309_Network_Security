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


------



## 3. Task 3: 实现 *OAEP Key Padding* 来保护 *textbook RSA* 的安全

- 基于 *textbook_RSA.py* 进行效果验证：

    - 若进行 *padding* 但不进行 *unpadding*（模拟被攻击者截取，无法 *unpadding*）：

        ```shell
        python textbook_RSA.py --encrypt_file ./test/plaintext.txt --OAEP_key_padding
        python textbook_RSA.py --decrypt_file ./test/ciphertext.txt
        ```

    - 同时进行 *padding* 和 *unpadding*（模拟正常的接收者）：

        ```shell
        python textbook_RSA.py --encrypt_file ./test/plaintext.txt --OAEP_key_padding --decrypt_OAEP
        python textbook_RSA.py --decrypt_file ./test/ciphertext.txt
        ```

- 在 *CCA2 attack* 中进行效果验证：

    - 若进行 *padding* 但不进行 *unpadding*（模拟被攻击者截取，无法 *unpadding*）：

        ```shell
        python CCA2_attack.py --OAEP_key_padding
        ```

    - 同时进行 *padding* 和 *unpadding*（模拟正常的接收者）：

        ```shell
        python CCA2_attack.py --OAEP_key_padding --decrypt_OAEP_for_receiver
        ```



