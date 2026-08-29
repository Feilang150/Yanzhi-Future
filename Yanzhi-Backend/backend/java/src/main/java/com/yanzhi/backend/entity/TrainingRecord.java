package com.yanzhi.backend.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 训练记录实体类
 * 
 * @author Yanzhi Team
 */
@Data
@TableName("training_record")
public class TrainingRecord {

    /** 训练ID */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /** 用户ID */
    private Long userId;

    /** 场景ID */
    private Long scenarioId;

    /** 训练状态：0-进行中，1-已完成，2-已中断 */
    private Integer status;

    /** 开始时间 */
    private LocalDateTime startTime;

    /** 结束时间 */
    private LocalDateTime endTime;

    /** 训练时长（秒） */
    private Integer duration;

    /** 对话次数 */
    private Integer dialogueCount;

    /** 综合得分 */
    private Double overallScore;

    /** 发音得分 */
    private Double pronunciationScore;

    /** 语法得分 */
    private Double grammarScore;

    /** 流利度得分 */
    private Double fluencyScore;

    /** 词汇丰富度得分 */
    private Double vocabularyScore;

    /** 逻辑连贯性得分 */
    private Double logicScore;

    /** 训练报告（MongoDB文档ID） */
    private String reportId;

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