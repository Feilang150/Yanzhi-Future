package com.yanzhi.backend.common;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

import java.io.Serializable;

/**
 * 通用响应结果类
 * 
 * @author Yanzhi Team
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Result<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 状态码 */
    private Integer code;

    /** 响应消息 */
    private String message;

    /** 响应数据 */
    private T data;

    /** 时间戳 */
    private Long timestamp;

    public Result() {
        this.timestamp = System.currentTimeMillis();
    }

    public Result(Integer code, String message) {
        this.code = code;
        this.message = message;
        this.timestamp = System.currentTimeMillis();
    }

    public Result(Integer code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
        this.timestamp = System.currentTimeMillis();
    }

    /**
     * 成功响应
     */
    public static <T> Result<T> success() {
        return new Result<>(200, "操作成功");
    }

    /**
     * 成功响应（带数据）
     */
    public static <T> Result<T> success(T data) {
        return new Result<>(200, "操作成功", data);
    }

    /**
     * 成功响应（自定义消息）
     */
    public static <T> Result<T> success(String message, T data) {
        return new Result<>(200, message, data);
    }

    /**
     * 失败响应
     */
    public static <T> Result<T> error() {
        return new Result<>(500, "操作失败");
    }

    /**
     * 失败响应（自定义消息）
     */
    public static <T> Result<T> error(String message) {
        return new Result<>(500, message);
    }

    /**
     * 失败响应（自定义状态码和消息）
     */
    public static <T> Result<T> error(Integer code, String message) {
        return new Result<>(code, message);
    }

    /**
     * 参数错误响应
     */
    public static <T> Result<T> paramError(String message) {
        return new Result<>(400, message);
    }

    /**
     * 未授权响应
     */
    public static <T> Result<T> unauthorized(String message) {
        return new Result<>(401, message);
    }

    /**
     * 禁止访问响应
     */
    public static <T> Result<T> forbidden(String message) {
        return new Result<>(403, message);
    }

    /**
     * 资源不存在响应
     */
    public static <T> Result<T> notFound(String message) {
        return new Result<>(404, message);
    }
}