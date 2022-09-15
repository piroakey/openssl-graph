# openssl-graph

`openssl speed`の結果からグラフ画像を生成するスクリプトです。

## 環境設定

### Linux

```bash
$ python -m venv venv
$ . venv/bin/activate
$ make env
```

### Windows(git bash)

```bash
$ python -m venv venv
$ . venv/Scripts/activate
$ make env
```

## 実行方法

1. `openssl speed`の標準出力をファイルにリダイレクトする。
2. ファイルをスクリプトに入力する。
3. グラフのPNG画像が生成される。

### ハンドシェイク

`s_time_ex`(オリジナルの計測用コマンド)が複数入力に対応しているので入力は1ファイルです。

```bash
$ ./s_time_ex > s_time_ex.txt
$ python openssl_graph.py handshake s_time_ex.txt
--> full.png
--> resumption.png
```

### 暗号アルゴリズム

複数ファイルに対応しています。

```bash
$ openssl speed -elapsed -evp aes-128-gcm -seconds 10 > aes-128-gcm.txt
$ openssl speed -elapsed -evp aes-256-gcm -seconds 10 > aes-256-gcm.txt
$ openssl speed -elapsed -evp chacha20-poly1305 -seconds 10 > chacha20-poly1305.txt
$ python openssl_graph.py crypto aes-128-gcm.txt aes-256-gcm.txt chacha20-poly1305.txt
--> crypto.png
```

```
AES-NIとPCLMULQDQ命令をオフにして
$ OPENSSL_ia32cap="~0x200000200000000" openssl speed -elapsed -evp aes-128-gcm -seconds 10 > aes-128-gcm.txt
$ OPENSSL_ia32cap="~0x200000200000000" openssl speed -elapsed -evp aes-256-gcm -seconds 10 > aes-256-gcm.txt
$ OPENSSL_ia32cap="~0x200000200000000" openssl speed -elapsed -evp chacha20-poly1305 -seconds 10 > chacha20-poly1305.txt
```

https://ja.wikipedia.org/wiki/CLMUL_instruction_set

https://www.openssl.org/docs/man3.0/man3/OPENSSL_ia32cap.html

### 鍵交換

`openssl speed`が複数入力に対応しているので入力は1ファイルです。

```bash
$ openssl speed ecdhp256 ecdhx25519 > keyex.txt
$ python openssl_graph.py keyex keyex.txt
--> keyex.png
```

### 署名/検証

`openssl speed`が複数入力に対応しているので入力は1ファイルです。

```bash
$ openssl speed ecdsap256 ed25519 > sign_verify.txt
$ python openssl_graph.py sign_verify sign_verify.txt
--> sign_verify.png
```
