package com.yanzhi.backend.controller;

import com.yanzhi.backend.common.Result;
import com.yanzhi.backend.service.TranslationService;
import com.yanzhi.backend.dto.*;
import com.yanzhi.backend.vo.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

/**
 * 翻译服务控制器
 * 
 * @author Yanzhi Team
 */
@Tag(name = "同声传译", description = "AI同声传译助手相关接口")
@RestController
@RequestMapping("/translation")
@RequiredArgsConstructor
public class TranslationController {

    private final TranslationService translationService;

    /**
     * 获取支持的语言列表
     */
    @Operation(summary = "支持的语言", description = "获取系统支持的所有语言")
    @GetMapping("/languages")
    public Result<List<LanguageVO>> getSupportedLanguages() {
        List<LanguageVO> languages = translationService.getSupportedLanguages();
        return Result.success(languages);
    }

    /**
     * 实时翻译
     */
    @Operation(summary = "实时翻译", description = "上传音频文件进行实时翻译")
    @PostMapping("/live")
    public Result<TranslationVO> translateAudio(@RequestParam("audio") MultipartFile audioFile,
                                               @RequestParam("targetLanguage") String targetLanguage,
                                               @RequestParam(value = "outputMode", defaultValue = "subtitle") String outputMode,
                                               HttpServletRequest request) {
        Long userId = translationService.getUserIdFromToken(request);
        TranslationVO translation = translationService.translateAudio(userId, audioFile, targetLanguage, outputMode);
        return Result.success(translation);
    }

    /**
     * 提交翻译纠错
     */
    @Operation(summary = "提交纠错", description = "用户提交翻译纠错，帮助模型优化")
    @PostMapping("/correct")
    public Result<Void> submitCorrection(@Validated @RequestBody TranslationCorrectionDTO correctionDTO,
                                        HttpServletRequest request) {
        Long userId = translationService.getUserIdFromToken(request);
        translationService.submitCorrection(userId, correctionDTO);
        return Result.success();
    }

    /**
     * 同步到口语训练
     */
    @Operation(summary = "同步到口语训练", description = "将翻译中的高频表达同步到口语训练场景")
    @GetMapping("/sync-training")
    public Result<List<ExpressionVO>> syncToSpeechTraining(HttpServletRequest request) {
        Long userId = translationService.getUserIdFromToken(request);
        List<ExpressionVO> expressions = translationService.syncToSpeechTraining(userId);
        return Result.success(expressions);
    }

    /**
     * 获取翻译历史
     */
    @Operation(summary = "翻译历史", description = "获取用户的翻译历史记录")
    @GetMapping("/history")
    public Result<List<TranslationHistoryVO>> getHistory(@RequestParam(defaultValue = "1") Integer page,
                                                         @RequestParam(defaultValue = "10") Integer pageSize,
                                                         HttpServletRequest request) {
        Long userId = translationService.getUserIdFromToken(request);
        List<TranslationHistoryVO> history = translationService.getHistory(userId, page, pageSize);
        return Result.success(history);
    }

    /**
     * 获取高频表达
     */
    @Operation(summary = "高频表达", description = "获取用户翻译中的高频表达")
    @GetMapping("/frequent-expressions")
    public Result<List<FrequentExpressionVO>> getFrequentExpressions(@RequestParam(defaultValue = "10") Integer limit,
                                                                     HttpServletRequest request) {
        Long userId = translationService.getUserIdFromToken(request);
        List<FrequentExpressionVO> expressions = translationService.getFrequentExpressions(userId, limit);
        return Result.success(expressions);
    }

    /**
     * 获取专业词库
     */
    @Operation(summary = "专业词库", description = "获取指定领域的专业词汇库")
    @GetMapping("/glossaries")
    public Result<List<GlossaryVO>> getGlossaries(@RequestParam("category") String category) {
        List<GlossaryVO> glossaries = translationService.getGlossaries(category);
        return Result.success(glossaries);
    }
}