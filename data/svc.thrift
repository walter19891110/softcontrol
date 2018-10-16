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

service SoftVersionControl{
    string verify_soft_code(1:string soft_id, 2:int verify_type, 3:string verify_code)
    string get_soft_info(1:string soft_id)
    string get_soft_list()
}