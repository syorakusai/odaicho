# notcore_lex.zip の分割について

GitHubの1ファイルあたりのアップロード上限（25MB）を超えるため、
`notcore_lex.zip`（約34MB）を2つに分割して置いています。

- notcore_lex.zip.partaa (20MB)
- notcore_lex.zip.partab (約14MB)

## 元のzipに戻す方法

### Mac / Linux
```
cat notcore_lex.zip.partaa notcore_lex.zip.partab > notcore_lex.zip
```

### Windows (コマンドプロンプト)
```
copy /b notcore_lex.zip.partaa+notcore_lex.zip.partab notcore_lex.zip
```

結合後、通常どおり解凍してください。
