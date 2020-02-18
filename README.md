# Robotframework2
### 文件结构
```
  ----robotframework2
   |
   |
   |----CustomerLib 【用户自定义的库以及公用方法存放的地方】
   |  |
   |  |
   |  |----CusLibrary
   |  |  |
   |  |  |----__init__.py【CusLibrary包的一些初始化信息，自定义类在此进行整合】
   |  |  |----CusBase.py 【继承Selenium2Library库对其进行修改封装】
   |  |  |----MySelenium.py【自定义类，继承CusBase】
   |  |  
   |  |
   |  |
   |  |
   |  |
   |  |
   |  |---__init__.txt【动态引入env_param模块，读取参数running_param，并在public_Action中引用】
   |  |---pub_Action.txt【这里引入Library           ../CustomerLib/    ${running_case_para}    run_on_failure=Capture Page Screenshot使用ride查看是会显示红色的，但不影响使用】
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
  
### 传入参数设置
* 参数是不会显示在代码里的，使用RIDE或者pycharm的配置的位置略有不同
* pybot更多的参数参考：[pybot参数](https://www.cnblogs.com/mianbaoshu/p/10983463.html)
* 例如我们以改变输出报告的路径为例
  1. 使用RIDE
     * 切换至“RUN”面板，在Arguments空格中输入：“-d reports”,这样就能在项目下新建一个reports文件夹，然后将log、report文件存在该文件夹下了。
  2. 使用Pycharm。更多参考：[相关网站图文说明](https://blog.csdn.net/liuyuqing2018/article/details/82773552)
     1. 需要先安装配置插件intelliBot
        ```
          菜单左上角点击 File>> Settings… 进入配置界面；
          进入Settings后，选择Plugins，在搜索栏输入intelliBot，点击下方Browse repositories 按钮。
        ```   
     2. 选择版本，点击install。安装完成后，根据引导重启
     3. RobotFramework的文件类型识别配置
        ```
         点击File>> Settings，选择Editor >> File Types ，
         在列表栏中找到 Robot Feature 选中，
         再点击右边栏上的加号，添加支持类型,分别添加 *.txt 和 *.
        ```
     4. **suite和case的执行配置**
        * 在我们在执行脚本时，可以单独执行一个case，也可以执行case的集合：suite（测试套），所以我们这里要做两个配置。
        1. Settings--选择External Tools，点击加号，添加可执行配置
        2. 配置单条case的执行：
           ```
            格式说明：
             Name：Robot Run SingleTestCase
             Program：pybot.bat path
             Arguments：-d results -t “SelectedText SelectedTextSelectedText” ./
             Working directory：FileDir FileDirFileDir
            实际配置：
             Name:Robot-run-testCase 
             Program:C:\Python27\Scripts\pybot.bat
             Arguments:-d $ProjectFileDir$\Reports -L Trace -t "$SelectedText$" TestCase 
             Workling directory:$ProjectFileDir$
           ```
        3. 配置suite（测试套）的执行：
           ```
            格式说明：
            Name：Robot Run TestSuite
            Program：pybot.bat path
            Arguments：-d results FileName FileNameFileName
            Working directory：FileDir FileDirFileDir
            实际配置：
            Name：Robot-run-testSuite 
            Program：C:\Python27\Scripts\pybot.bat
            Arguments：-d $ProjectFileDir$\Reports  -L Trace $FileName$ 
            Arguments：$FileDir$
           ```
### 注意事项
1. 自定义关键字，在python代码中定义函数名为：aaa_bbb_ccc，但是在关键字使用的时候会是：Aaa Bbb Ccc。例如 copy_drivers_to_local,使用时候为Copy Drivers To Local          
2. 注意：在RIDE里面配置路径的时候必须要写绝对路径，而是用pycharm的参数是不对的，如：$ProjectFileDir$\Reports