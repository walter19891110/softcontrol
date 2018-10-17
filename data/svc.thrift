/**
 * thrift支持的数据类型：
 *
 *  bool          布尔类型
 *  i8 (byte)     整型8位
 *  i16           整型16位
 *  i32           整型32位
 *  i64           整型64位
 *  double        64位的浮点数
 *  string        字符串
 *  binary        字节
 *  map<t1,t2>    Map集合
 *  list<t1>      List集合
 *  set<t1>       Set集合
 */

/**
* 为数据类型定义别名,定义好之后，文档中可以直接使用别名
**/
typedef i32 int

/**
* 定义数据结构，类似面向对象编程中的类
* 1、属性需要一个表示数字（如：1，2，3）；这个数字在同个作用域内不能重复
* 2、属性默认都是必输属性，如果需要属性可选在属性前面加上optional关键字
* 3、可以为属性指定默认值，格式是在属性名称后面用等号。如：num1 =0,0就是num1的默认值
**/
struct SoftInfoDict{
    1:string softid,     // 软件ID
    2:string softname,   // 软件名称
    3:string osname,     // 软件运行的操作系统
    4:int  softmode,     // 软件模式
    5:string setupname,  // 安装包名
    6:string setupcode,  // 安装包校验码
    7:string mainfile,   // 主程序文件名
    8:string maincode,   // 主程序文件校验码
    9:string desc        //软件描述
}


/**
* 定义服务service。
* 1、服务可以继承，只能单继承
* 2、引用其他thrift文件的服务时需要加上文件名。如： share.haredService;share就是文件名
*/

service SoftVersionControl{
    // 版本控制
    string verify_soft_code(1:string soft_id, 2:int verify_type, 3:string verify_code)
    string get_soft_info(1:string soft_id)
    string get_soft_list()

    // 软件信息管理
    string add_soft_info(1:SoftInfoDict soft_dict)
    string modify_soft_mode(1:string soft_id, 2:int soft_mode)
    string del_soft_info(1:string soft_id)
    string add_soft_code(1:string soft_id, 2:int verify_type, 3:string verify_code)
    string del_soft_code(1:string soft_id, 2:int verify_type, 3:string verify_code)
}