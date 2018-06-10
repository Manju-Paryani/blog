# visual studio 创建和使用 DLL 文件


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

* [visual studio 创建和使用 DLL 文件](#visual-studio-创建和使用-dll-文件)
	* [创建 DLL 文件](#创建-dll-文件)
	* [将执行文件链接到到 DLL](#将执行文件链接到到-dll)
		* [隐式链接](#隐式链接)
		* [显式链接](#显式链接)
	* [利用 Dependency Walker 查看依赖关系](#利用-dependency-walker-查看依赖关系)
	* [参考链接](#参考链接)

<!-- /code_chunk_output -->


## 创建 DLL 文件

[Creating and Using a Dynamic Link Library (C++)](https://msdn.microsoft.com/en-us/library/ms235636.aspx)

## 将执行文件链接到到 DLL

[Linking an Executable to a DLL](https://msdn.microsoft.com/en-us/library/9yd93633.aspx)

可执行文件通过以下两种方式之一链接到（或加载）DLL:
* [隐式链接](https://msdn.microsoft.com/en-us/library/d14wsce5.aspx)
* [显式链接](https://msdn.microsoft.com/en-us/library/784bt7z7.aspx)

隐式链接有时被称为静态加载或加载时动态链接。显式链接有时被称为动态加载或运行时动态链接

### 隐式链接
将上面生成的 DLL 文件对应的 .lib 文件包含到需要使用 DLL 文件的 project 中，并把 .dll 文件和可执行文件放到一起即可。
[Youtube -- Implicit loading of Dll file using Visual Studio](https://www.youtube.com/watch?v=rS_lE2UOzgg)

### 显式链接

示例：
```c++
typedef UINT (CALLBACK* LPFNDLLFUNC1)(DWORD,UINT);  
...  

HINSTANCE hDLL;               // Handle to DLL  
LPFNDLLFUNC1 lpfnDllFunc1;    // Function pointer  
DWORD dwParam1;  
UINT  uParam2, uReturnVal;  

hDLL = LoadLibrary("MyDLL");  
if (hDLL != NULL)  
{  
   lpfnDllFunc1 = (LPFNDLLFUNC1)GetProcAddress(hDLL,  
                                           "DLLFunc1");  
   if (!lpfnDllFunc1)  
   {  
      // handle the error  
      FreeLibrary(hDLL);         
      return SOME_ERROR_CODE;  
   }  
   else  
   {  
      // call the function  
      uReturnVal = lpfnDllFunc1(dwParam1, uParam2);  
   }  
}  
```

## 利用 Dependency Walker 查看依赖关系

Dependency Walker是一个免费的实用程序，可扫描任何32位或64位Windows模块（exe，dll，ocx，sys等），并构建所有相关模块的分层树状图。对于找到的每个模块，它列出了该模块导出的所有功能，以及其中哪些功能实际上由其他模块调用。另一个视图显示所需文件的最小集合，以及有关每个文件的详细信息，包括文件的完整路径，基本地址，版本号，机器类型，调试信息等。对于加载和执行模块相关的系统错误，Dependency Walker也非常有用。 Dependency Walker检测许多常见的应用程序问题，如缺少模块，无效模块，导入/导出不匹配，循环依赖性错误，模块的机器类型不匹配以及模块初始化失败。 Dependency Walker可在Windows 95,98，Me，NT，2000，XP，2003，Vista，7和8上运行。它可以处理任何32位或64位Windows模块，包括专为Windows CE设计的模块。

[Dependency Walker official](http://www.dependencywalker.com/)

## 参考链接
* [为何Windows下的动态库总伴随一个静态库？](http://blog.shengbin.me/posts/windows-dll-with-lib)


[上一级](base.md)
[上一篇](insertUSBDevicesNotResponse.md)
[下一篇](vmvare_windows.md)