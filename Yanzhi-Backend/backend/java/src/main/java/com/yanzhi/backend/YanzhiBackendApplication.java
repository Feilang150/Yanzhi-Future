package com.yanzhi.backend;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.socket.config.annotation.EnableWebSocket;

/**
 * Yanzhi Future 后端应用主类
 * 
 * @author Yanzhi Team
 * @since 2024-07-01
 */
@SpringBootApplication
@EnableTransactionManagement
@EnableCaching
@EnableAsync
@EnableScheduling
@EnableWebSocket
@MapperScan("com.yanzhi.backend.mapper")
public class YanzhiBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(YanzhiBackendApplication.class, args);
        System.out.println("Yanzhi Future Backend Started Successfully!");
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}