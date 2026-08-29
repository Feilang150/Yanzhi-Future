// MongoDB 集合初始化脚本

// 切换到数据库
use yanzhi_future;

// 创建训练报告集合（用于存储详细的训练报告）
db.createCollection("training_reports", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["training_id", "user_id", "report_date"],
      properties: {
        training_id: { bsonType: "long" },
        user_id: { bsonType: "long" },
        report_date: { bsonType: "date" },
        summary: {
          bsonType: "object",
          properties: {
            total_duration: { bsonType: "int" },
            dialogue_count: { bsonType: "int" },
            overall_score: { bsonType: "double" }
          }
        },
        dialogues: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              role: { bsonType: "string" },
              content: { bsonType: "string" },
              timestamp: { bsonType: "date" }
            }
          }
        },
        evaluations: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              category: { bsonType: "string" },
              score: { bsonType: "double" },
              feedback: { bsonType: "string" }
            }
          }
        },
        corrections: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              error_type: { bsonType: "string" },
              original: { bsonType: "string" },
              corrected: { bsonType: "string" },
              explanation: { bsonType: "string" }
            }
          }
        },
        improvement_suggestions: {
          bsonType: "array",
          items: { bsonType: "string" }
        }
      }
    }
  }
});

// 创建小说文本集合（用于存储上传的小说原文）
db.createCollection("novel_texts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "title", "content"],
      properties: {
        user_id: { bsonType: "long" },
        title: { bsonType: "string" },
        author: { bsonType: "string" },
        content: { bsonType: "string" },
        file_name: { bsonType: "string" },
        file_size: { bsonType: "long" },
        upload_date: { bsonType: "date" },
        status: { bsonType: "string" } // uploaded, processing, completed
      }
    }
  }
});

// 创建对话历史集合（用于存储口语陪练的对话历史）
db.createCollection("dialogue_history", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["training_id", "user_id", "dialogues"],
      properties: {
        training_id: { bsonType: "long" },
        user_id: { bsonType: "long" },
        scenario_id: { bsonType: "long" },
        dialogues: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              role: { bsonType: "string" }, // user, ai
              text: { bsonType: "string" },
              audio_path: { bsonType: "string" },
              timestamp: { bsonType: "date" },
              evaluation: {
                bsonType: "object",
                properties: {
                  pronunciation_score: { bsonType: "double" },
                  fluency_score: { bsonType: "double" }
                }
              }
            }
          }
        }
      }
    }
  }
});

// 创建剧本草稿集合（用于存储正在编辑的剧本草稿）
db.createCollection("script_drafts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "title", "content"],
      properties: {
        user_id: { bsonType: "long" },
        script_id: { bsonType: "long" },
        title: { bsonType: "string" },
        content: { bsonType: "object" }, // YAML解析后的对象
        yaml_content: { bsonType: "string" }, // 原始YAML内容
        last_modified: { bsonType: "date" },
        auto_save: { bsonType: "bool" }
      }
    }
  }
});

// 创建用户行为分析集合（用于存储用户行为数据，用于个性化推荐）
db.createCollection("user_behavior", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "action", "timestamp"],
      properties: {
        user_id: { bsonType: "long" },
        action: { bsonType: "string" }, // login, training_start, translation_start, script_create, etc.
        module: { bsonType: "string" }, // speech_coach, translation, script_creator
        details: { bsonType: "object" },
        timestamp: { bsonType: "date" }
      }
    }
  }
});

// 创建高频表达集合（用于存储和统计高频词汇/表达）
db.createCollection("frequent_expressions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["expression", "language", "count"],
      properties: {
        expression: { bsonType: "string" },
        translation: { bsonType: "string" },
        language: { bsonType: "string" },
        category: { bsonType: "string" }, // general, business, academic, etc.
        count: { bsonType: "int" },
        last_used: { bsonType: "date" },
        users: { bsonType: "array", items: { bsonType: "long" } }
      }
    }
  }
});

// 创建专业词库集合（用于存储各领域的专业词汇）
db.createCollection("glossaries", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["term", "translation", "category"],
      properties: {
        term: { bsonType: "string" },
        translation: { bsonType: "string" },
        category: { bsonType: "string" }, // medical, legal, technical, etc.
        language_pair: { bsonType: "string" }, // en-zh, zh-en, etc.
        definition: { bsonType: "string" },
        example: { bsonType: "string" },
        created_at: { bsonType: "date" }
      }
    }
  }
});

// 创建索引优化查询性能
db.training_reports.createIndex({ training_id: 1 });
db.training_reports.createIndex({ user_id: 1, report_date: -1 });

db.novel_texts.createIndex({ user_id: 1 });
db.novel_texts.createIndex({ upload_date: -1 });

db.dialogue_history.createIndex({ training_id: 1 });
db.dialogue_history.createIndex({ user_id: 1, timestamp: -1 });

db.script_drafts.createIndex({ user_id: 1 });
db.script_drafts.createIndex({ script_id: 1 });

db.user_behavior.createIndex({ user_id: 1, timestamp: -1 });
db.user_behavior.createIndex({ action: 1, timestamp: -1 });

db.frequent_expressions.createIndex({ expression: 1 });
db.frequent_expressions.createIndex({ language: 1, count: -1 });

db.glossaries.createIndex({ term: 1 });
db.glossaries.createIndex({ category: 1 });
db.glossaries.createIndex({ language_pair: 1 });

// 插入一些示例高频表达
db.frequent_expressions.insertMany([
  {
    expression: "Good morning, everyone",
    translation: "大家早上好",
    language: "en",
    category: "general",
    count: 15,
    last_used: new Date(),
    users: [1, 2, 3]
  },
  {
    expression: "Thank you for your attention",
    translation: "感谢您的关注",
    language: "en",
    category: "business",
    count: 12,
    last_used: new Date(),
    users: [1, 4, 5]
  },
  {
    expression: "Let me introduce myself",
    translation: "让我自我介绍一下",
    language: "en",
    category: "general",
    count: 10,
    last_used: new Date(),
    users: [2, 3, 6]
  }
]);

// 插入一些示例专业词汇
db.glossaries.insertMany([
  {
    term: "Artificial Intelligence",
    translation: "人工智能",
    category: "technical",
    language_pair: "en-zh",
    definition: "计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统",
    example: "AI is transforming many industries.",
    created_at: new Date()
  },
  {
    term: "Machine Learning",
    translation: "机器学习",
    category: "technical",
    language_pair: "en-zh",
    definition: "人工智能的一个子集，专注于使计算机能够从数据中学习",
    example: "Machine learning algorithms improve with experience.",
    created_at: new Date()
  },
  {
    term: "Natural Language Processing",
    translation: "自然语言处理",
    category: "technical",
    language_pair: "en-zh",
    definition: "计算机科学、人工智能和语言学的交叉领域，致力于计算机与人类语言之间的交互",
    example: "NLP is used in chatbots and translation services.",
    created_at: new Date()
  }
]);

print("MongoDB collections initialized successfully!");