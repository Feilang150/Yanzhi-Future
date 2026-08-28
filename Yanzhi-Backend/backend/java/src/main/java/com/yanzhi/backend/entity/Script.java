package com.yanzhi.backend.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 剧本实体类
 * 
 * @author Yanzhi Team
 */
@Data
@TableName("script")
public class Script {

    /** 剧本ID */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /** 用户ID */
    private Long userId;

    /** 剧本标题 */
    private String title;

    /** 作者 */
    private String author;

    /** 版本号 */
    private String version;

    /** 剧本类型 */
    private String genre;

    /** 剧本梗概 */
    private String synopsis;

    /** 剧本内容（YAML格式） */
    private String content;

    /** 人物数量 */
    private Integer characterCount;

    /** 场景数量 */
    private Integer sceneCount;

    /** 字数统计 */
    private Integer wordCount;

    /** 小说原文ID（MongoDB） */
    private String novelTextId;

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