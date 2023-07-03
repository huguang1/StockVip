
--
-- Table structure for table `stock_officialshareprice`
--

DROP TABLE IF EXISTS `stock_officialshareprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_officialshareprice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
    `add_time` date NOT NULL,
      `price` decimal(16,2) NOT NULL,
        `c_time` datetime(6) NOT NULL,
          `u_time` datetime(6) NOT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
            /*!40101 SET character_set_client = @saved_cs_client */;

            --
            -- Dumping data for table `stock_officialshareprice`
            --

            LOCK TABLES `stock_officialshareprice` WRITE;
            /*!40000 ALTER TABLE `stock_officialshareprice` DISABLE KEYS */;
            INSERT INTO `stock_officialshareprice` VALUES (1,'2019-04-02',5.60,'2019-04-03 04:25:48.773361','2019-04-03 04:25:48.773386'),(3,'2019-04-03',5.68,'2019-04-03 06:12:24.915600','2019-04-03 06:12:24.915653'),(4,'2019-04-04',5.67,'2019-04-04 06:14:45.617032','2019-04-04 06:14:45.617060'),(6,'2019-04-05',5.88,'2019-04-05 06:25:53.951911','2019-04-05 06:25:53.951961'),(7,'2019-04-06',5.65,'2019-04-06 06:55:47.843298','2019-04-06 06:55:47.843343'),(9,'2019-04-07',5.85,'2019-04-08 06:13:37.717707','2019-04-08 06:13:37.717758'),(10,'2019-04-08',5.73,'2019-04-08 06:13:58.340762','2019-04-08 06:13:58.340810'),(11,'2019-04-09',5.82,'2019-04-09 07:02:04.732966','2019-04-09 07:02:04.732995'),(12,'2019-04-10',5.69,'2019-04-10 05:49:45.745089','2019-04-10 05:49:45.745126'),(13,'2019-04-11',5.89,'2019-04-11 05:56:25.457257','2019-04-11 05:56:25.457292'),(14,'2019-04-12',5.66,'2019-04-12 05:35:05.002677','2019-04-12 05:35:05.002702'),(15,'2019-04-13',5.55,'2019-04-13 06:09:02.106254','2019-04-13 06:09:02.106306'),(16,'2019-04-14',5.48,'2019-04-14 06:02:09.705373','2019-04-14 06:02:09.705428'),(17,'2019-04-15',5.68,'2019-04-15 06:00:30.369617','2019-04-15 06:00:30.369664'),(18,'2019-04-16',5.69,'2019-04-16 05:48:19.631753','2019-04-16 05:48:19.631807'),(19,'2019-04-17',5.53,'2019-04-17 05:59:09.697082','2019-04-17 05:59:09.697134'),(20,'2019-04-18',5.60,'2019-04-18 06:18:18.850124','2019-04-18 06:18:18.850153'),(21,'2019-04-19',5.83,'2019-04-19 05:53:56.056884','2019-04-19 05:53:56.056908'),(22,'2019-04-20',6.01,'2019-04-20 05:37:36.301013','2019-04-20 05:37:36.301057'),(23,'2019-04-21',6.06,'2019-04-21 05:37:45.654719','2019-04-21 05:37:45.654766'),(24,'2019-04-22',6.08,'2019-04-22 06:04:10.917988','2019-04-22 06:04:10.918030'),(25,'2019-04-23',6.09,'2019-04-23 05:48:17.509114','2019-04-23 05:48:17.509158'),(26,'2019-04-24',6.13,'2019-04-24 06:23:17.203073','2019-04-24 06:23:17.203116'),(27,'2019-04-25',6.13,'2019-04-25 06:22:01.277595','2019-04-25 06:22:01.277642'),(28,'2019-04-26',6.25,'2019-04-26 05:50:06.894684','2019-04-26 05:50:06.894730'),(29,'2019-04-27',6.29,'2019-04-27 06:05:58.813367','2019-04-27 06:05:58.813421'),(30,'2019-04-28',6.13,'2019-04-28 05:58:07.721862','2019-04-28 05:58:07.721886'),(31,'2019-04-29',6.16,'2019-04-29 06:10:40.855010','2019-04-29 06:10:40.855034'),(32,'2019-04-30',6.25,'2019-04-30 05:38:27.508993','2019-04-30 05:38:27.509039');
            /*!40000 ALTER TABLE `stock_officialshareprice` ENABLE KEYS */;
            UNLOCK TABLES;

            --
            -- Table structure for table `stock_personalgain`
            --

            DROP TABLE IF EXISTS `stock_personalgain`;
            /*!40101 SET @saved_cs_client     = @@character_set_client */;
            /*!40101 SET character_set_client = utf8 */;
            CREATE TABLE `stock_personalgain` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
                `valid_bet` bigint(20) NOT NULL,
                  `grade_one` decimal(10,2) NOT NULL,
                    `grade_two` decimal(10,2) NOT NULL,
                      `grade_three` decimal(10,2) NOT NULL,
                        `grade_four` decimal(10,2) NOT NULL,
                          `grade_five` decimal(10,2) NOT NULL,
                            `c_time` datetime(6) NOT NULL,
                              `u_time` datetime(6) NOT NULL,
                                PRIMARY KEY (`id`)
                                ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
                                /*!40101 SET character_set_client = @saved_cs_client */;

                                --
                                -- Dumping data for table `stock_personalgain`
                                --

                                LOCK TABLES `stock_personalgain` WRITE;
                                /*!40000 ALTER TABLE `stock_personalgain` DISABLE KEYS */;
                                INSERT INTO `stock_personalgain` VALUES (1,0,-2.00,-2.00,-2.00,-2.00,-2.00,'2019-03-04 06:25:02.167607','2019-03-04 06:25:02.167632'),(2,1,0.00,0.00,0.00,0.00,0.00,'2019-03-04 06:32:18.293450','2019-03-04 06:32:18.293514'),(3,10000,0.10,0.10,0.10,0.10,0.10,'2019-03-04 06:33:01.103815','2019-03-04 06:33:01.103840'),(4,50000,0.50,0.50,0.50,0.50,0.50,'2019-03-04 06:33:21.299595','2019-03-04 06:33:21.299621'),(5,100000,0.80,0.80,0.80,0.80,0.80,'2019-03-04 06:33:48.051405','2019-03-04 06:33:48.051430'),(6,500000,1.00,1.00,1.00,1.00,1.00,'2019-03-04 06:34:08.623306','2019-03-04 06:34:08.623330'),(7,1000000,1.20,1.20,1.20,1.20,1.20,'2019-03-04 06:34:30.810301','2019-03-04 06:34:30.810325'),(8,5000000,1.30,1.30,1.30,1.30,1.30,'2019-03-04 06:35:00.612511','2019-03-04 06:35:00.612535'),(9,10000000,2.00,2.00,2.00,2.00,2.00,'2019-03-04 06:35:20.305031','2019-03-04 06:35:20.305060'),(10,50000000,5.00,5.00,5.00,5.00,5.00,'2019-03-04 06:35:38.913176','2019-03-04 06:35:38.913201');
                                /*!40000 ALTER TABLE `stock_personalgain` ENABLE KEYS */;
                                UNLOCK TABLES;

                                --
                                -- Table structure for table `stock_transactionhour`
                                --

                                DROP TABLE IF EXISTS `stock_transactionhour`;
                                /*!40101 SET @saved_cs_client     = @@character_set_client */;
                                /*!40101 SET character_set_client = utf8 */;
                                CREATE TABLE `stock_transactionhour` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT,
                                    `start_time` datetime(6) NOT NULL,
                                      `end_time` datetime(6) NOT NULL,
                                        `close_desc` varchar(255) COLLATE utf8_bin NOT NULL,
                                          `is_maintain` tinyint(1) NOT NULL,
                                            `maintain_desc` varchar(255) COLLATE utf8_bin NOT NULL,
                                              `start_a` time(6) NOT NULL,
                                                `end_a` time(6) NOT NULL,
                                                  `c_time` datetime(6) NOT NULL,
                                                    `u_time` datetime(6) NOT NULL,
                                                      PRIMARY KEY (`id`)
                                                      ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
                                                      /*!40101 SET character_set_client = @saved_cs_client */;

                                                      --
                                                      -- Dumping data for table `stock_transactionhour`
                                                      --

                                                      LOCK TABLES `stock_transactionhour` WRITE;
                                                      /*!40000 ALTER TABLE `stock_transactionhour` DISABLE KEYS */;
                                                      INSERT INTO `stock_transactionhour` VALUES (1,'2018-01-09 12:00:00.000000','2022-02-09 12:00:00.000000','对不起，系统升级!',0,'对不起，请在活动范围时间内参与活动!!!','15:00:00.000000','23:59:59.000000','2019-03-31 16:47:03.000000','2019-03-31 16:47:06.000000');
                                                      /*!40000 ALTER TABLE `stock_transactionhour` ENABLE KEYS */;
                                                      UNLOCK TABLES;


                                                      --
                                                      -- Table structure for table `mosaic_assetscategory`
                                                      --

                                                      DROP TABLE IF EXISTS `mosaic_assetscategory`;
                                                      /*!40101 SET @saved_cs_client     = @@character_set_client */;
                                                      /*!40101 SET character_set_client = utf8 */;
                                                      CREATE TABLE `mosaic_assetscategory` (
                                                        `id` int(11) NOT NULL AUTO_INCREMENT,
                                                          `name` varchar(128) COLLATE utf8_bin NOT NULL,
                                                            `c_time` datetime(6) NOT NULL,
                                                              PRIMARY KEY (`id`),
                                                                KEY `mosaic_assetscategory_name_c_time_621c40dd_idx` (`name`,`c_time`)
                                                                ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
                                                                /*!40101 SET character_set_client = @saved_cs_client */;

                                                                --
                                                                -- Dumping data for table `mosaic_assetscategory`
                                                                --

                                                                LOCK TABLES `mosaic_assetscategory` WRITE;
                                                                /*!40000 ALTER TABLE `mosaic_assetscategory` DISABLE KEYS */;
                                                                INSERT INTO `mosaic_assetscategory` VALUES (3,'体育赛事','2019-03-03 15:00:02.000000'),(4,'彩票游戏','2019-03-03 15:00:17.000000'),(5,'棋牌游戏','2019-03-03 14:59:48.000000'),(1,'电子游艺','2019-03-03 14:59:31.000000'),(2,'视讯直播','2019-03-03 14:59:48.000000');
                                                                /*!40000 ALTER TABLE `mosaic_assetscategory` ENABLE KEYS */;
                                                                UNLOCK TABLES;

