package com.yanzhi.backend.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 场景实体类
 * 
 * @author Yanzhi Team
 */
@Data
@TableName("scenario")
public class Scenario {

    /** 场景ID */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /** 场景名称 */
    private String name;

    /** 场景描述 */
    private String description;

    /** 场景类型：0-预设，1-自定义 */
    private Integer type;

    /** 场景图标 */
    private String icon;

    /** 难度级别：1-简单，2-中等，3-困难 */
    private Integer difficulty;

    /** 预计时长（分钟） */
    private Integer duration;

    /** 分类标签 */
    private String category;

    /** 核心词汇（JSON数组） */
    private String keywords;

    /** 背景描述 */
    private String background;

    /** 创建者ID（自定义场景） */
    private Long creatorId;

    /** 使用次数 */
    private Integer usageCount;

    /** 评分（1-5星） */
    private Double rating;

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