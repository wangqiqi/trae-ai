# 编码规范与最佳实践

## 通用规范

### 命名规范
- 变量和函数使用驼峰命名法：`userName`, `getUserInfo()`
- 类和构造函数使用帕斯卡命名法：`UserService`, `HttpClient`
- 常量使用全大写加下划线：`MAX_RETRY_COUNT`, `API_BASE_URL`
- 文件和目录使用短横线分隔：`user-service.ts`, `api-client.js`

### 代码格式
- 使用2个空格缩进（前端）或4个空格缩进（后端）
- 每行代码不超过100个字符
- 函数长度不超过50行
- 文件长度不超过300行

### 注释规范
- 公共API必须有JSDoc或TypeDoc注释
- 复杂业务逻辑需要注释说明
- TODO/FIXME标记需要包含作者和截止日期

## 前端规范

### React规范
```typescript
// ✅ 好的做法
interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
  loading?: boolean;
}

export const UserCard: React.FC<UserCardProps> = ({ 
  user, 
  onEdit, 
  loading = false 
}) => {
  return (
    <div className="user-card">
      {loading ? <Spinner /> : <UserInfo user={user} />}
    </div>
  );
};
```

### CSS规范
- 使用BEM命名法：`block__element--modifier`
- 避免使用ID选择器
- 移动端优先的响应式设计

## 后端规范

### API设计规范
```typescript
// ✅ RESTful API设计
@Get('users/:id')
@HttpCode(200)
async getUserById(
  @Param('id') id: string,
  @Query('include') include?: string[]
): Promise<UserResponse> {
  return this.userService.findById(id, { include });
}
```

### 数据库规范
- 表名使用复数：`users`, `orders`
- 外键使用`表名单数_id`：`user_id`, `order_id`
- 创建时间和更新时间必须包含
- 软删除使用`deleted_at`字段

## 测试规范

### 单元测试
- 测试文件名：`*.test.ts` 或 `*.spec.ts`
- 测试覆盖率：业务逻辑>80%，工具函数>90%
- 每个测试只测试一个功能点

### 测试命名
```typescript
// ✅ 清晰的测试描述
describe('UserService', () => {
  describe('createUser', () => {
    it('应该创建新用户并返回用户对象', async () => {
      // ...
    });
    
    it('当邮箱已存在时应该抛出ConflictException', async () => {
      // ...
    });
  });
});
```

## Git规范

### 提交信息
```
类型(范围): 简短描述

详细描述（可选）

Fixes #123
```

#### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或辅助工具

### 分支管理
- `main`: 生产环境代码
- `develop`: 开发分支
- `feature/功能名`: 功能开发分支
- `hotfix/修复名`: 紧急修复分支

## 安全规范

### 前端安全
- 所有用户输入必须转义
- 使用CSP策略
- HTTPS强制跳转
- 敏感信息不在控制台输出

### 后端安全
- 所有接口必须验证权限
- 使用参数化查询防止SQL注入
- 密码使用bcrypt加密
- JWT token设置合理过期时间

## 性能规范

### 前端性能
- 首屏加载时间<3秒
- 图片使用WebP格式
- 使用CDN加速静态资源
- 实现懒加载和代码分割

### 后端性能
- API响应时间<500ms
- 数据库查询优化，避免N+1问题
- 使用Redis缓存热点数据
- 实现接口限流和熔断