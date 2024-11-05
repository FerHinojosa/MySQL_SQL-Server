-- Eliminar las tablas 'hashtag' y 'tweet' si ya existen
DROP TABLE IF EXISTS nao.hashtag;
DROP TABLE IF EXISTS nao.tweet;

-- Crear la tabla 'tweet' en la base de datos 'nao'
CREATE TABLE nao.tweet (
    `id` INT NOT NULL AUTO_INCREMENT,  -- Identificador único y clave primaria para cada tweet
    `id_tweet` VARCHAR(30) NOT NULL,   -- ID único del tweet en la plataforma
    `texto` VARCHAR(1000),             -- Contenido del tweet (texto)
    `usuario` VARCHAR(100),            -- Nombre del usuario que publicó el tweet
    `fecha` DATETIME,                  -- Fecha y hora de publicación del tweet
    `retweets` INT DEFAULT 0,          -- Número de retweets (por defecto 0 si no hay retweets)
    `favoritos` INT DEFAULT 0,         -- Número de favoritos o 'likes' (por defecto 0 si no hay favoritos)
    PRIMARY KEY (`id`)                 -- Definir 'id' como la clave primaria
) CHARSET=utf8mb4;                     -- Utilizar el charset utf8mb4 para soportar emojis y caracteres especiales

-- Crear la tabla 'hashtag' en la base de datos 'nao'
CREATE TABLE nao.hashtag (
    `id` INT NOT NULL AUTO_INCREMENT,  -- Identificador único y clave primaria para cada hashtag
    `hashtag` VARCHAR(255),            -- Texto del hashtag utilizado en el tweet
    `tweet_id` INT,                    -- Relación con el 'id' del tweet en la tabla 'tweet'
    PRIMARY KEY (`id`),                -- Definir 'id' como la clave primaria
    INDEX `idx_tweet_id` (`tweet_id`), -- Índice para optimizar las consultas por 'tweet_id'
    CONSTRAINT `fk_hashtag_tweet`
        FOREIGN KEY (`tweet_id`) REFERENCES nao.tweet(`id`)  -- Clave foránea que relaciona 'hashtag' con 'tweet'
        ON DELETE CASCADE                                    -- Eliminar hashtags relacionados si se elimina el tweet
        ON UPDATE CASCADE                                    -- Actualizar hashtags relacionados si cambia el tweet
) CHARSET=utf8mb4;                     -- Utilizar el charset utf8mb4 para soportar emojis y caracteres especiales
