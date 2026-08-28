package com.yanzhi.backend.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 翻译记录实体类
 * 
 * @author Yanzhi Team
 */
@Data
@TableName("translation_record")
public class TranslationRecord {

    /** 翻译ID */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /** 用户ID */
    private Long userId;

    /** 源语言 */
    private String sourceLanguage;

    /** 目标语言 */
    private String targetLanguage;

    /** 原始文本 */
    private String originalText;

    /** 翻译文本 */
    private String translatedText;

    /** 音频URL */
    private String audioUrl;

    /** 输出模式：subtitle-字幕，voice-语音，both-双模式 */
    private String outputMode;

    /** 翻译时长（毫秒） */
    private Integer duration;

    /** 质量评分 */
    private Double qualityScore;

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