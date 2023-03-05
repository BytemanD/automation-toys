# automation-toys

python 实现的自动化工具

## 交通票解析工具

解析增值税PDF电子发票

```bash
auto-toys parse-traffic-tickets <PDF路径1> [<PDF路径2> ...]
```

说明：

1. 支持多个PDF路径，可以是文件、目录或者通配符(例如: *xyz.pdf)正则表达式；
2. 支持输出表格或者csv格式
3. 支持将PDF剪切并且合并到同一个PDF中（A4纸，每页4张）

更多用法可通过 `--help` 参数查看。

![img](./doc/parse-traffic-tickets.png)