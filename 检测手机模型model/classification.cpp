#include <caffe/caffe.hpp>
#ifdef USE_OPENCV
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#endif  // USE_OPENCV
#include <algorithm>
#include <iosfwd>
#include <memory>
#include <string>
#include <utility>
#include <vector>
#include <fstream>
#include <exception>
#ifdef USE_OPENCV
using namespace caffe;  // NOLINT(build/namespaces)
using std::string;
float get_sums_img_number(string model_file, string trained_file, string mean_file, string label_file, vector<cv::String> filename, float prediction_second);
typedef std::pair<string, float> Prediction;
void get_classifier_pic(Prediction p, int i, int lebaltests, string errfilepath, float prediction_second, string trained_file, cv::Mat img);

class Classifier {
public:
	Classifier(const string& model_file,
		const string& trained_file,
		const string& mean_file,
		const string& label_file);

	std::vector<Prediction> Classify(const cv::Mat& img, int N = 2);

private:
	void SetMean(const string& mean_file);

	std::vector<float> Predict(const cv::Mat& img);

	void WrapInputLayer(std::vector<cv::Mat>* input_channels);

	void Preprocess(const cv::Mat& img,
		std::vector<cv::Mat>* input_channels);

private:
	shared_ptr<Net<float> > net_;
	cv::Size input_geometry_;
	int num_channels_;
	cv::Mat mean_;
	std::vector<string> labels_;
};

Classifier::Classifier(const string& model_file,
	const string& trained_file,
	const string& mean_file,
	const string& label_file) {
#ifdef CPU_ONLY
	Caffe::set_mode(Caffe::CPU);
#else
	Caffe::set_mode(Caffe::GPU);
#endif

	/* Load the network. */
	net_.reset(new Net<float>(model_file, TEST));
	net_->CopyTrainedLayersFrom(trained_file);

	CHECK_EQ(net_->num_inputs(), 1) << "Network should have exactly one input.";
	CHECK_EQ(net_->num_outputs(), 1) << "Network should have exactly one output.";

	Blob<float>* input_layer = net_->input_blobs()[0];
	num_channels_ = input_layer->channels();
	CHECK(num_channels_ == 3 || num_channels_ == 1)
		<< "Input layer should have 1 or 3 channels.";
	input_geometry_ = cv::Size(input_layer->width(), input_layer->height());

	/* Load the binaryproto mean file. */
	if (mean_file != "")
	{
		SetMean(mean_file);
	}

	/* Load labels. */
	std::ifstream labels(label_file.c_str());
	CHECK(labels) << "Unable to open labels file " << label_file;
	string line;
	while (std::getline(labels, line))
		labels_.push_back(string(line));

	Blob<float>* output_layer = net_->output_blobs()[0];
	CHECK_EQ(labels_.size(), output_layer->channels())
		<< "Number of labels is different from the output layer dimension.";
}

static bool PairCompare(const std::pair<float, int>& lhs,
	const std::pair<float, int>& rhs) {
	return lhs.first > rhs.first;
}

/* Return the indices of the top N values of vector v. */
static std::vector<int> Argmax(const std::vector<float>& v, int N) {
	std::vector<std::pair<float, int> > pairs;
	for (size_t i = 0; i < v.size(); ++i)
		pairs.push_back(std::make_pair(v[i], static_cast<int>(i)));
	std::partial_sort(pairs.begin(), pairs.begin() + N, pairs.end(), PairCompare);

	std::vector<int> result;
	for (int i = 0; i < N; ++i)
		result.push_back(pairs[i].second);
	return result;
}

/* Return the top N predictions. */
std::vector<Prediction> Classifier::Classify(const cv::Mat& img, int N) {
	std::vector<float> output = Predict(img);

	N = std::min<int>(labels_.size(), N);
	std::vector<int> maxN = Argmax(output, N);
	std::vector<Prediction> predictions;
	for (int i = 0; i < N; ++i) {
		int idx = maxN[i];
		predictions.push_back(std::make_pair(labels_[idx], output[idx]));
	}

	return predictions;
}

/* Load the mean file in binaryproto format. */
void Classifier::SetMean(const string& mean_file) {
	BlobProto blob_proto;
	ReadProtoFromBinaryFileOrDie(mean_file.c_str(), &blob_proto);

	/* Convert from BlobProto to Blob<float> */
	Blob<float> mean_blob;
	mean_blob.FromProto(blob_proto);
	CHECK_EQ(mean_blob.channels(), num_channels_)
		<< "Number of channels of mean file doesn't match input layer.";

	/* The format of the mean file is planar 32-bit float BGR or grayscale. */
	std::vector<cv::Mat> channels;
	float* data = mean_blob.mutable_cpu_data();
	for (int i = 0; i < num_channels_; ++i) {
		/* Extract an individual channel. */
		cv::Mat channel(mean_blob.height(), mean_blob.width(), CV_32FC1, data);
		channels.push_back(channel);
		data += mean_blob.height() * mean_blob.width();
	}

	/* Merge the separate channels into a single image. */
	cv::Mat mean;
	cv::merge(channels, mean);

	/* Compute the global mean pixel value and create a mean image
	* filled with this value. */
	cv::Scalar channel_mean = cv::mean(mean);
	mean_ = cv::Mat(input_geometry_, mean.type(), channel_mean);
}

std::vector<float> Classifier::Predict(const cv::Mat& img) {
	Blob<float>* input_layer = net_->input_blobs()[0];
	input_layer->Reshape(1, num_channels_,
		input_geometry_.height, input_geometry_.width);
	/* Forward dimension change to all layers. */
	net_->Reshape();

	std::vector<cv::Mat> input_channels;
	WrapInputLayer(&input_channels);

	Preprocess(img, &input_channels);

	net_->Forward();

	/* Copy the output layer to a std::vector */
	Blob<float>* output_layer = net_->output_blobs()[0];
	const float* begin = output_layer->cpu_data();
	const float* end = begin + output_layer->channels();
	return std::vector<float>(begin, end);
}

/* Wrap the input layer of the network in separate cv::Mat objects
* (one per channel). This way we save one memcpy operation and we
* don't need to rely on cudaMemcpy2D. The last preprocessing
* operation will write the separate channels directly to the input
* layer. */
void Classifier::WrapInputLayer(std::vector<cv::Mat>* input_channels) {
	Blob<float>* input_layer = net_->input_blobs()[0];

	int width = input_layer->width();
	int height = input_layer->height();
	float* input_data = input_layer->mutable_cpu_data();
	for (int i = 0; i < input_layer->channels(); ++i) {
		cv::Mat channel(height, width, CV_32FC1, input_data);
		input_channels->push_back(channel);
		input_data += width * height;
	}
}

void Classifier::Preprocess(const cv::Mat& img,
	std::vector<cv::Mat>* input_channels) {
	/* Convert the input image to the input image format of the network. */
	cv::Mat sample;
	if (img.channels() == 3 && num_channels_ == 1)
		cv::cvtColor(img, sample, cv::COLOR_BGR2GRAY);
	else if (img.channels() == 4 && num_channels_ == 1)
		cv::cvtColor(img, sample, cv::COLOR_BGRA2GRAY);
	else if (img.channels() == 4 && num_channels_ == 3)
		cv::cvtColor(img, sample, cv::COLOR_BGRA2BGR);
	else if (img.channels() == 1 && num_channels_ == 3)
		cv::cvtColor(img, sample, cv::COLOR_GRAY2BGR);
	else
		sample = img;

	cv::Mat sample_resized;
	if (sample.size() != input_geometry_)
		cv::resize(sample, sample_resized, input_geometry_);
	else
		sample_resized = sample;

	cv::Mat sample_float;
	if (num_channels_ == 3)
		sample_resized.convertTo(sample_float, CV_32FC3);
	else
		sample_resized.convertTo(sample_float, CV_32FC1);

	cv::Mat sample_normalized;
	if (!mean_.empty())
	{
		cv::subtract(sample_float, mean_, sample_normalized);
	}
	else sample_normalized = sample_float;
	/* This operation will write the separate BGR planes directly to the
	* input layer of the network because it is wrapped by the cv::Mat
	* objects in input_channels. */
	cv::split(sample_normalized, *input_channels);

	CHECK(reinterpret_cast<float*>(input_channels->at(0).data)
		== net_->input_blobs()[0]->cpu_data())
		<< "Input channels are not wrapping the input layer of the network.";
}
string confuse_pic_path = "E:\\ynphonemodels\\error\\other\\";//保存未分类的路径
string yhand_pic_path = "E:\\ynphonemodels\\error\\yhand\\";//保存正确分类的路径
string yobject_pic_path = "E:\\ynphonemodels\\error\\yobject\\";//保存正确分类的路径
string yphone_pic_path = "E:\\ynphonemodels\\error\\yphone\\";//保存正确分类的路径
int main(int argc, char** argv) {
	string model_file = "E:\\ynphonemodels\\_iter_232000.caffemodel";
	string deploy_file = "E:\\ynphonemodels\\deploy.prototxt";
	string mean_file = "";
	string lable_file = "E:\\ynphonemodels\\sysKabel.txt";
	string pic_path = "E:\\ynphonemodels\\error\\temp";//保存未分类的路径
	vector<cv::String> Yfilename;
	cv::glob(pic_path, Yfilename, true);
	get_sums_img_number(deploy_file, model_file, mean_file, lable_file, Yfilename, 0.5);//此处的倒数第二个参数无用（标签值）
	getchar();
}
#else
int main(int argc, char** argv) {
	LOG(FATAL) << "This example requires OpenCV; compile with USE_OPENCV.";
}
#endif  // USE_OPENCV
//Classifier初始化
//参数说明：
//model_file：deploy.prototxt文件
//trained_file：caffemodel文件
//mean_file：mean文件
//label_file：标签文件
//filename：图片文件夹
//prediction_second：预值（阀值）
float get_sums_img_number(string model_file, string trained_file, string mean_file, string label_file, vector<cv::String> filename, float prediction_second){
	Classifier classifier(model_file, trained_file, mean_file, label_file);
	float error_img = 0;
	for (int i = 0; i < filename.size(); i++)
	{
		//char ii[255];
		cv::Mat img = cv::imread(filename[i], -1);
		cv::resize(img, img, cv::Size(100, 100), 0, 0, 1);
		std::vector<Prediction> predictions = classifier.Classify(img);
		/* Print the top N predictions. */
		
		Prediction p = predictions[0];
		get_classifier_pic(p, i, 1, yhand_pic_path, prediction_second, trained_file, img);
		get_classifier_pic(p, i, 2, yobject_pic_path, prediction_second, trained_file, img);
		get_classifier_pic(p, i, 3, yphone_pic_path, prediction_second, trained_file, img);
	}
	std::cout << "======end======" << std::endl;
	return 0;
}
//输入分类后的图片
//参数说明：
//p：预测类
//i：输入图片编号
//lebaltests：自定义标签
//errfilepath：输出文件夹
//prediction_second：预定义阀值
//trained_file：caffemodel文件
//img：输入的Mat
void get_classifier_pic(Prediction p, int i, int lebaltests, string errfilepath, float prediction_second, string trained_file, cv::Mat img){
	int leba = atoi(p.first.c_str());
	std::stringstream ss;
	std::string str;
	ss << i;
	ss >> str;
	string output_img = "";
	string temp = errfilepath + "_" + trained_file.substr(trained_file.find_first_of("_"), 11) + "_" + str + ".jpg";
	if (abs(leba - lebaltests) < 0.001)
	{
		output_img = temp;
	}
	else
	{
		if (p.second < prediction_second)
		{
			output_img = temp;
		}
		else
		{
			//输出当标签为lebaltests检错的图像
			output_img = confuse_pic_path + "_" + trained_file.substr(trained_file.find_first_of("_"), 11) + "_" + str + ".jpg";
		}
	}
	imwrite(output_img, img);
}