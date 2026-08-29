package com.yanzhi.backend.controller;

import com.yanzhi.backend.common.Result;
import com.yanzhi.backend.entity.User;
import com.yanzhi.backend.service.UserService;
import com.yanzhi.backend.dto.LoginDTO;
import com.yanzhi.backend.dto.UpdateUserInfoDTO;
import com.yanzhi.backend.vo.UserInfoVO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;

/**
 * 用户控制器
 * 
 * @author Yanzhi Team
 */
@Tag(name = "用户管理", description = "用户登录、信息管理相关接口")
@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * 微信小程序登录
     */
    @Operation(summary = "微信登录", description = "通过微信code进行用户登录")
    @PostMapping("/login")
    public Result<UserInfoVO> login(@Validated @RequestBody LoginDTO loginDTO) {
        UserInfoVO userInfoVO = userService.login(loginDTO);
        return Result.success(userInfoVO);
    }

    /**
     * 获取用户信息
     */
    @Operation(summary = "获取用户信息", description = "获取当前登录用户的详细信息")
    @GetMapping("/info")
    public Result<UserInfoVO> getUserInfo(HttpServletRequest request) {
        Long userId = userService.getUserIdFromToken(request);
        UserInfoVO userInfoVO = userService.getUserInfo(userId);
        return Result.success(userInfoVO);
    }

    /**
     * 更新用户信息
     */
    @Operation(summary = "更新用户信息", description = "更新用户的基本信息")
    @PutMapping("/info")
    public Result<Void> updateUserInfo(@Validated @RequestBody UpdateUserInfoDTO updateUserInfoDTO, 
                                       HttpServletRequest request) {
        Long userId = userService.getUserIdFromToken(request);
        userService.updateUserInfo(userId, updateUserInfoDTO);
        return Result.success();
    }

    /**
     * 更新用户偏好设置
     */
    @Operation(summary = "更新用户偏好", description = "更新用户的偏好设置")
    @PutMapping("/preferences")
    public Result<Void> updatePreferences(@RequestBody String preferences, 
                                          HttpServletRequest request) {
        Long userId = userService.getUserIdFromToken(request);
        userService.updatePreferences(userId, preferences);
        return Result.success();
    }

    /**
     * 获取训练记录
     */
    @Operation(summary = "获取训练记录", description = "获取用户的训练历史记录")
    @GetMapping("/training-records")
    public Result<Object> getTrainingRecords(@RequestParam(defaultValue = "1") Integer page,
                                            @RequestParam(defaultValue = "10") Integer pageSize,
                                            HttpServletRequest request) {
        Long userId = userService.getUserIdFromToken(request);
        Object records = userService.getTrainingRecords(userId, page, pageSize);
        return Result.success(records);
    }

    /**
     * 获取剧本列表
     */
    @Operation(summary = "获取剧本列表", description = "获取用户创作的剧本列表")
    @GetMapping("/scripts")
    public Result<Object> getScripts(@RequestParam(defaultValue = "1") Integer page,
                                    @RequestParam(defaultValue = "10") Integer pageSize,
                                    HttpServletRequest request) {
        Long userId = userService.getUserIdFromToken(request);
        Object scripts = userService.getScripts(userId, page, pageSize);
        return Result.success(scripts);
    }
}