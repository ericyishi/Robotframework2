# Robotframework2
### 文件结构
```
  ----robotframework2
   |
   |
   |----CustomerLib 【用户自定义的库以及公用方法存放的地方】
   |  |
   |  |---__init__.txt
   |  |---pub_Action.txt
   |  |---pub_Data.txt
   |  |---pub_Data.txt
   |  |---pub_Flow.txt   
   |   
   |   
   |----Report 【存放输出的报告】   
   |   
   |   
   |----TestCase【测试用例】   
   |  |   
   |  |---001_moduleName【模块名】   
   |     |---1.01_componentName.txt【当前模块下的组件名,里面是写实际的用例】  
   |     |---__init__.txt   
   |     |---Lib【用于存放当前模块的分层模型】  
   |        |---moduleName_Action.txt【3.动作层，单个对元素的操作】
   |        |---moduleName_Data.txt【1.数据层，用于存放变量】
   |        |---moduleName_Element.txt【2.元素层，用于界面要控制的元素】
   |        |---moduleName_Flow.txt【4.流程层，是把多个动作拼在一起】
   |   
   |      
   
   
```
* 资源Resource和库Library的引用
  1. 通常用例只引用当前模块Lib下Flow，而Flow只引用Action
  2. 而Action会去引用pub_Flow,以及当前模块的Element和Data
  

