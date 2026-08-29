package com.yanzhi.backend.controller;

import com.yanzhi.backend.common.Result;
import com.yanzhi.backend.service.ScriptCreatorService;
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
 * 剧本创作控制器
 * 
 * @author Yanzhi Team
 */
@Tag(name = "剧本创作", description = "AI小说转剧本工具相关接口")
@RestController
@RequestMapping("/script")
@RequiredArgsConstructor
public class ScriptCreatorController {

    private final ScriptCreatorService scriptCreatorService;

    /**
     * 生成剧本
     */
    @Operation(summary = "生成剧本", description = "上传小说文本，AI自动生成剧本")
    @PostMapping("/generate")
    public Result<ScriptVO> generateScript(@RequestParam("file") MultipartFile file,
                                          HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        ScriptVO script = scriptCreatorService.generateScript(userId, file);
        return Result.success(script);
    }

    /**
     * 获取剧本列表
     */
    @Operation(summary = "剧本列表", description = "获取用户创作的所有剧本")
    @GetMapping("/list")
    public Result<List<ScriptVO>> getScriptList(@RequestParam(defaultValue = "1") Integer page,
                                              @RequestParam(defaultValue = "10") Integer pageSize,
                                              HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        List<ScriptVO> scripts = scriptCreatorService.getScriptList(userId, page, pageSize);
        return Result.success(scripts);
    }

    /**
     * 获取剧本详情
     */
    @Operation(summary = "剧本详情", description = "获取指定剧本的详细信息")
    @GetMapping("/detail")
    public Result<ScriptDetailVO> getScriptDetail(@RequestParam("scriptId") Long scriptId,
                                                 HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        ScriptDetailVO detail = scriptCreatorService.getScriptDetail(userId, scriptId);
        return Result.success(detail);
    }

    /**
     * 编辑剧本
     */
    @Operation(summary = "编辑剧本", description = "更新剧本内容")
    @PutMapping("/edit")
    public Result<ScriptVO> editScript(@Validated @RequestBody EditScriptDTO editScriptDTO,
                                      HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        ScriptVO script = scriptCreatorService.editScript(userId, editScriptDTO);
        return Result.success(script);
    }

    /**
     * 保存剧本
     */
    @Operation(summary = "保存剧本", description = "保存剧本内容")
    @PostMapping("/save")
    public Result<Void> saveScript(@Validated @RequestBody SaveScriptDTO saveScriptDTO,
                                  HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        scriptCreatorService.saveScript(userId, saveScriptDTO);
        return Result.success();
    }

    /**
     * 删除剧本
     */
    @Operation(summary = "删除剧本", description = "删除指定的剧本")
    @DeleteMapping("/delete")
    public Result<Void> deleteScript(@RequestParam("scriptId") Long scriptId,
                                    HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        scriptCreatorService.deleteScript(userId, scriptId);
        return Result.success();
    }

    /**
     * 导入到口语训练
     */
    @Operation(summary = "导入训练", description = "将剧本对话导入口语陪练进行角色扮演训练")
    @PostMapping("/import-training")
    public Result<TrainingScenarioVO> importToTraining(@Validated @RequestBody ImportTrainingDTO importTrainingDTO,
                                                       HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        TrainingScenarioVO scenario = scriptCreatorService.importToTraining(userId, importTrainingDTO);
        return Result.success(scenario);
    }

    /**
     * 导出剧本
     */
    @Operation(summary = "导出剧本", description = "导出剧本为指定格式")
    @GetMapping("/export")
    public Result<String> exportScript(@RequestParam("scriptId") Long scriptId,
                                     @RequestParam(value = "format", defaultValue = "yaml") String format,
                                     HttpServletRequest request) {
        Long userId = scriptCreatorService.getUserIdFromToken(request);
        String content = scriptCreatorService.exportScript(userId, scriptId, format);
        return Result.success(content);
    }

    /**
     * 获取剧本模板
     */
    @Operation(summary = "剧本模板", description = "获取可用的剧本模板")
    @GetMapping("/templates")
    public Result<List<ScriptTemplateVO>> getScriptTemplates() {
        List<ScriptTemplateVO> templates = scriptCreatorService.getScriptTemplates();
        return Result.success(templates);
    }

    /**
     * 验证剧本格式
     */
    @Operation(summary = "验证格式", description = "验证剧本YAML格式是否正确")
    @PostMapping("/validate")
    public Result<ValidationResultVO> validateScript(@RequestBody String content) {
        ValidationResultVO result = scriptCreatorService.validateScript(content);
        return Result.success(result);
    }
}