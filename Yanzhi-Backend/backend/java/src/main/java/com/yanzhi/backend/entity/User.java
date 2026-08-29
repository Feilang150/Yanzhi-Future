package com.yanzhi.backend.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 用户实体类
 * 
 * @author Yanzhi Team
 */
@Data
@TableName("user")
public class User {

    /** 用户ID */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /** 微信openid */
    private String openid;

    /** 用户昵称 */
    private String nickname;

    /** 头像URL */
    private String avatar;

    /** 性别：0-未知，1-男，2-女 */
    private Integer gender;

    /** 年龄 */
    private Integer age;

    /** 手机号 */
    private String phone;

    /** 邮箱 */
    private String email;

    /** 用户偏好设置（JSON格式） */
    private String preferences;

    /** 账号状态：0-正常，1-禁用 */
    private Integer status;

    /** 删除标记：0-未删除，1-已删除 */
    @TableLogic
    private Integer deleted;

    /** 创建时间 */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    /** 更新时间 */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}