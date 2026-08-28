package com.yanzhi.backend.controller;

import com.yanzhi.backend.common.Result;
import com.yanzhi.backend.service.SpeechCoachService;
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
 * 口语陪练控制器
 * 
 * @author Yanzhi Team
 */
@Tag(name = "口语陪练", description = "AI英语口语陪练相关接口")
@RestController
@RequestMapping("/speech-coach")
@RequiredArgsConstructor
public class SpeechCoachController {

    private final SpeechCoachService speechCoachService;

    /**
     * 获取场景列表
     */
    @Operation(summary = "获取场景列表", description = "获取所有可用的训练场景")
    @GetMapping("/scenarios")
    public Result<List<ScenarioVO>> getScenarios() {
        List<ScenarioVO> scenarios = speechCoachService.getScenarios();
        return Result.success(scenarios);
    }

    /**
     * 创建自定义场景
     */
    @Operation(summary = "创建自定义场景", description = "用户创建自己的训练场景")
    @PostMapping("/scenarios")
    public Result<ScenarioVO> createScenario(@Validated @RequestBody CreateScenarioDTO createScenarioDTO,
                                              HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        ScenarioVO scenario = speechCoachService.createScenario(userId, createScenarioDTO);
        return Result.success(scenario);
    }

    /**
     * 开始训练会话
     */
    @Operation(summary = "开始训练", description = "创建新的训练会话")
    @PostMapping("/training/start")
    public Result<TrainingSessionVO> startTraining(@Validated @RequestBody StartTrainingDTO startTrainingDTO,
                                                   HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        TrainingSessionVO session = speechCoachService.startTraining(userId, startTrainingDTO);
        return Result.success(session);
    }

    /**
     * 发送语音进行对话
     */
    @Operation(summary = "发送语音", description = "发送用户语音，获取AI回复和评测")
    @PostMapping("/training/send-voice")
    public Result<DialogueResponseVO> sendVoice(@RequestParam("audio") MultipartFile audioFile,
                                               @RequestParam("sessionId") Long sessionId,
                                               HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        DialogueResponseVO response = speechCoachService.sendVoice(userId, sessionId, audioFile);
        return Result.success(response);
    }

    /**
     * 发音评测
     */
    @Operation(summary = "发音评测", description = "对用户发音进行专业评测")
    @PostMapping("/evaluate")
    public Result<EvaluationVO> evaluatePronunciation(@RequestParam("audio") MultipartFile audioFile,
                                                     @RequestParam("sessionId") Long sessionId,
                                                     HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        EvaluationVO evaluation = speechCoachService.evaluatePronunciation(userId, sessionId, audioFile);
        return Result.success(evaluation);
    }

    /**
     * 语法纠错
     */
    @Operation(summary = "语法纠错", description = "对用户文本进行语法和表达纠错")
    @PostMapping("/correct")
    public Result<CorrectionVO> correctGrammar(@Validated @RequestBody GrammarCorrectionDTO correctionDTO,
                                               HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        CorrectionVO correction = speechCoachService.correctGrammar(userId, correctionDTO);
        return Result.success(correction);
    }

    /**
     * 结束训练
     */
    @Operation(summary = "结束训练", description = "结束当前训练会话，生成训练报告")
    @PostMapping("/training/end")
    public Result<Void> endTraining(@RequestParam("sessionId") Long sessionId,
                                   HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        speechCoachService.endTraining(userId, sessionId);
        return Result.success();
    }

    /**
     * 获取训练报告
     */
    @Operation(summary = "获取训练报告", description = "获取详细的训练报告")
    @GetMapping("/training/report")
    public Result<TrainingReportVO> getTrainingReport(@RequestParam("sessionId") Long sessionId,
                                                      HttpServletRequest request) {
        Long userId = speechCoachService.getUserIdFromToken(request);
        TrainingReportVO report = speechCoachService.getTrainingReport(userId, sessionId);
        return Result.success(report);
    }
}