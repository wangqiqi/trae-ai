# 📡 API接口规范模板

## 🎯 API基本信息
- **API名称**: [API系统名称]
- **版本**: v1.0.0
- **基础URL**: https://api.example.com/v1
- **文档更新日期**: [当前日期]
- **维护团队**: [团队名称]

## 🔐 认证授权

### 认证方式
- **类型**: JWT Token认证
- **Token获取**: POST /auth/login
- **Token刷新**: POST /auth/refresh
- **Token有效期**: 24小时

### 请求头格式
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

## 📋 通用规范

### 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1635760800
}
```

### 错误码定义
| 状态码 | 描述 | 说明 |
|--------|------|------|
| 200 | 成功 | 请求正常处理 |
| 400 | 参数错误 | 请求参数不合法 |
| 401 | 未授权 | Token无效或已过期 |
| 403 | 权限不足 | 用户权限不足 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 500 | 服务器错误 | 内部服务器错误 |

### 分页参数
```
?page=1&size=20&sort=created_at&order=desc
```

### 时间格式
- **标准格式**: ISO 8601 (2021-11-01T12:00:00Z)
- **时区**: UTC+8

## 🚀 接口详情

### 👤 用户认证模块

#### 用户注册
```
POST /auth/register
```

**请求参数**:
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "confirm_password": "string"
}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user_id": "uuid",
    "username": "string",
    "email": "user@example.com",
    "created_at": "2021-11-01T12:00:00Z"
  }
}
```

#### 用户登录
```
POST /auth/login
```

**请求参数**:
```json
{
  "email": "user@example.com",
  "password": "string"
}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "jwt_token_string",
    "refresh_token": "refresh_token_string",
    "expires_in": 86400,
    "user_info": {
      "user_id": "uuid",
      "username": "string",
      "email": "user@example.com"
    }
  }
}
```

### 📊 用户管理模块

#### 获取用户信息
```
GET /users/{user_id}
```

**响应数据**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": "uuid",
    "username": "string",
    "email": "user@example.com",
    "avatar": "https://example.com/avatar.jpg",
    "profile": {
      "first_name": "string",
      "last_name": "string",
      "phone": "string",
      "bio": "string"
    },
    "created_at": "2021-11-01T12:00:00Z",
    "updated_at": "2021-11-01T12:00:00Z"
  }
}
```

#### 更新用户信息
```
PUT /users/{user_id}
```

**请求参数**:
```json
{
  "username": "string",
  "profile": {
    "first_name": "string",
    "last_name": "string",
    "phone": "string",
    "bio": "string"
  }
}
```

### 📁 资源管理模块

#### 创建资源
```
POST /resources
```

**请求参数**:
```json
{
  "title": "string",
  "description": "string",
  "category": "string",
  "tags": ["tag1", "tag2"]
}
```

#### 获取资源列表
```
GET /resources
```

**查询参数**:
```
?page=1&size=20&category=web&tags=vue,react&sort=created_at&order=desc
```

**响应数据**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "string",
        "description": "string",
        "category": "string",
        "tags": ["tag1", "tag2"],
        "author": {
          "user_id": "uuid",
          "username": "string"
        },
        "created_at": "2021-11-01T12:00:00Z",
        "updated_at": "2021-11-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

#### 获取单个资源
```
GET /resources/{resource_id}
```

#### 更新资源
```
PUT /resources/{resource_id}
```

#### 删除资源
```
DELETE /resources/{resource_id}
```

## 🧪 测试用例

### 测试环境
- **测试URL**: https://api-test.example.com/v1
- **测试账号**: test@example.com / test123

### 测试工具
- **API测试**: Postman, Insomnia
- **自动化测试**: pytest, Jest
- **性能测试**: Apache JMeter

### 测试场景
1. **认证测试**: 注册、登录、Token刷新
2. **CRUD测试**: 创建、读取、更新、删除
3. **分页测试**: 不同分页参数
4. **错误处理**: 各种错误情况

## 🔧 错误处理示例

### 400 Bad Request
```json
{
  "code": 400,
  "message": "参数验证失败",
  "errors": {
    "email": ["邮箱格式不正确"],
    "password": ["密码长度不能少于8位"]
  }
}
```

### 401 Unauthorized
```json
{
  "code": 401,
  "message": "Token已过期",
  "data": {
    "refresh_required": true
  }
}
```

### 404 Not Found
```json
{
  "code": 404,
  "message": "用户不存在",
  "data": {
    "user_id": "uuid"
  }
}
```

## 📚 相关文档
- [认证授权指南](auth-guide.md)
- [错误码详解](error-codes.md)
- [SDK开发指南](sdk-guide.md)
- [版本更新日志](changelog.md)

## 📞 技术支持
- **API维护团队**: [团队联系方式]
- **文档更新**: [文档维护者]
- **问题反馈**: [反馈渠道]