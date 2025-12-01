package com.ibm.wxd.datalabs.demo.cass_spark_iceberg.utils;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Utility class for Spark session creation and Cassandra table reading
 */
public class SparkUtil {
    private static Logger LOGGER = LoggerFactory.getLogger(SparkUtil.class);
    
    /**
     * Create a Spark session configured for Iceberg and Cassandra
     */
    public SparkSession createSparkSession(String appName) {
        LOGGER.info("Creating Spark session: {}", appName);
        
        // Get Cassandra host from system property or use default
        String cassandraHost = System.getProperty("spark.cassandra.connection.host", "localhost");
        LOGGER.info("Cassandra host: {}", cassandraHost);
        
        SparkSession spark = SparkSession.builder()
            .appName(appName)
            .config("spark.cassandra.connection.host", cassandraHost)
            .config("spark.sql.extensions", 
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.catalog.spark_catalog", 
                "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.spark_catalog.type", "hadoop")
            .getOrCreate();
        
        LOGGER.info("Spark session created successfully");
        LOGGER.info("Spark version: {}", spark.version());
        
        return spark;
    }
    
    /**
     * Read a Cassandra table into a Spark DataFrame with optimized settings
     */
    public Dataset<Row> readCassandraTable(SparkSession spark, String keyspace, String table) {
        LOGGER.info("Reading Cassandra table: {}.{}", keyspace, table);
        
        Dataset<Row> df = spark.read()
            .format("org.apache.spark.sql.cassandra")
            .option("keyspace", keyspace)
            .option("table", table)
            // Performance optimizations for partition-key scanning
            .option("spark.cassandra.input.split.size_in_mb", "64")  // Smaller splits for better parallelism
            .option("spark.cassandra.input.fetch.size_in_rows", "1000")  // Fetch more rows per request
            .option("spark.cassandra.concurrent.reads", "512")  // Increase concurrent reads
            .load();
        
        LOGGER.info("Successfully loaded table: {}.{}", keyspace, table);
        
        return df;
    }
    
    /**
     * Read a Cassandra table with time-bucket filtering for even better performance
     * 
     * This method leverages the partition key (asset_id, time_bucket) by filtering
     * on time_bucket values, which dramatically reduces the number of partitions scanned.
     * 
     * @param spark SparkSession
     * @param keyspace Cassandra keyspace name
     * @param table Cassandra table name
     * @param timeBucketPrefix Prefix filter for time_bucket (e.g., "2024-12" for December 2024)
     * @return Filtered DataFrame
     */
    public Dataset<Row> readCassandraTableFiltered(SparkSession spark, String keyspace, 
                                                    String table, String timeBucketPrefix) {
        LOGGER.info("Reading Cassandra table: {}.{} with time_bucket filter: {}*", 
                   keyspace, table, timeBucketPrefix);
        
        Dataset<Row> df = spark.read()
            .format("org.apache.spark.sql.cassandra")
            .option("keyspace", keyspace)
            .option("table", table)
            .option("spark.cassandra.input.split.size_in_mb", "64")
            .option("spark.cassandra.input.fetch.size_in_rows", "1000")
            .option("spark.cassandra.concurrent.reads", "512")
            .load()
            .filter("time_bucket LIKE '" + timeBucketPrefix + "%'");  // Filter on partition key component
        
        LOGGER.info("Successfully loaded and filtered table: {}.{}", keyspace, table);
        
        return df;
    }
}

