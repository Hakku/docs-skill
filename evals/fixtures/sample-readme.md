# dataflow

dataflow is a command-line tool for building and running data pipelines. It was originally created to solve the problem of connecting multiple data sources together without writing boilerplate code. The tool supports reading from CSV files, JSON APIs, SQL databases, and streaming sources like Kafka. It has been used in production at several companies and handles millions of records per day. If you want to get started, you should first make sure you have Python 3.10 or newer installed on your system, and then you can install it using pip.

The main idea behind dataflow is that you define your pipeline as a YAML configuration file and then run it from the command line. Each step in the pipeline is called a "stage" and stages can be chained together. The output of one stage becomes the input of the next stage. You can also define conditional branches and error handling within the YAML file. The configuration format was inspired by GitHub Actions but with some important differences that make it more suitable for data processing workloads.

```bash
pip install dataflow-cli
dataflow init my-pipeline
cd my-pipeline
dataflow run pipeline.yaml
```

To configure dataflow you need to create a configuration file called dataflow.config.yaml in your project root directory. This file contains settings for authentication, logging, retry behavior, and output formats. The authentication section supports API keys, OAuth tokens, and basic auth credentials. You should set the log_level to "debug" during development and change it to "warning" for production. The retry section allows you to configure how many times a failed stage should be retried before the pipeline fails, with the default being 3 retries with exponential backoff. The output_format can be set to "json", "csv", or "parquet" depending on your needs, and you can also configure compression using gzip or snappy.

dataflow supports a plugin system that allows you to extend its functionality. Plugins are Python packages that follow a specific naming convention and implement a standard interface. To create a plugin you need to create a Python package with the name dataflow-plugin-yourname and implement the DataflowPlugin base class. The plugin system was redesigned in version 2.0 to be more flexible and now supports both synchronous and asynchronous plugins.

```python
from dataflow.plugins import DataflowPlugin

class MyPlugin(DataflowPlugin):
    name = "my-plugin"

    def process(self, record):
        record["processed"] = True
        return record
```

There are several environment variables that control dataflow behavior. DATAFLOW_HOME sets the directory where dataflow stores its cache and temporary files, defaulting to ~/.dataflow. DATAFLOW_LOG_LEVEL overrides the log level from the config file. DATAFLOW_PARALLEL_WORKERS controls how many parallel workers are used for processing, with the default being the number of CPU cores. DATAFLOW_MAX_MEMORY_MB sets the maximum memory usage before dataflow starts spilling to disk. DATAFLOW_PLUGIN_PATH can be set to a colon-separated list of directories where dataflow looks for plugins in addition to the default locations.

The pipeline YAML format supports several advanced features. You can use template variables with the ${VAR} syntax to reference environment variables or values from previous stages. Conditional execution is supported via the `when` keyword which accepts Python expressions. You can define reusable stage templates in a separate file and reference them with the `uses` keyword. Error handling is done through the `on_error` keyword which can be set to "skip", "retry", or "fail".

For monitoring and observability, dataflow provides a built-in metrics endpoint that exposes Prometheus-compatible metrics. You can enable it by setting metrics.enabled to true in your config file and optionally configuring the port with metrics.port (default 9090). The metrics include pipeline_records_processed_total, pipeline_stage_duration_seconds, and pipeline_errors_total. You can also configure custom metrics in your plugins using the metrics API.

If you encounter issues, the most common problems are related to authentication configuration and network timeouts. Make sure your API keys are correctly set in the config file or as environment variables. For timeout issues, try increasing the timeout_seconds value in the config file. You can also run dataflow with the --verbose flag to get more detailed output about what is happening during pipeline execution.
