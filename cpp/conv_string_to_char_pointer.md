# 将string转换为char指针
* ## If you need const char*

```cpp

const char *mycharpointer=mystring.c_str();

```

* ## If you need modifiable char*

```cpp

std:vector<char> v(mystring.length()+1);
std:strcpy(&v[0],mystring.c_str());
char *pc=&v[0];

```


[上一级](README.md)
[上一篇](constructorThrowException.md)
[下一篇](createOwnIterator.md)
