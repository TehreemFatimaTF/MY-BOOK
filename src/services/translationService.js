/**
 * Translation Service
 * Handles translation between English and Urdu
 */

import React from 'react';

// Simple translation mapping for demonstration
// In a real implementation, this would come from a backend API or translation service
const TRANSLATION_MAP = {
  'Chapter 1: Introduction to ROS 2': 'باب 1: ROS 2 کا تعارف',
  'What is ROS 2?': 'ROS 2 کیا ہے؟',
  'Key Features of ROS 2': 'ROS 2 کی کلیدی خصوصیات',
  'Why ROS 2 for Physical AI?': 'فزیکل AI کے لیے ROS 2 کیوں؟',
  'ROS 2 Architecture': 'ROS 2 آرکیٹیکچر',
  'The DDS Layer': 'DDS لیئر',
  'Getting Started with ROS 2': 'ROS 2 کے ساتھ شروعات',
  'Installation': 'تنصیب',
  'Basic Commands': 'بنیادی کمانڈز',
  'ROS 2 vs. ROS 1': 'ROS 2 بمقابلہ ROS 1',
  'Next Steps': 'اگلے اقدامات',
  'Summary': 'خلاصہ',
  'In this chapter, you learned:': 'اس باب میں آپ نے سیکھا:',
  'What ROS 2 is and why it\'s important for Physical AI': 'ROS 2 کیا ہے اور فزیکل AI کے لیے یہ کیوں اہم ہے',
  'The key features and architecture of ROS 2': 'ROS 2 کی کلیدی خصوصیات اور آرکیٹیکچر',
  'How ROS 2 serves as the "nervous system" for humanoid robots': 'کیسے ROS 2 ہیومنوائڈ روبوٹس کے لیے "نروس سسٹم" کا کام کرتا ہے',
  'Basic ROS 2 commands to get started': 'شروع کرنے کے لیے بنیادی ROS 2 کمانڈز',
  'Welcome to the first chapter of Module 1: The Robotic Nervous System. In this chapter, we\'ll introduce you to the Robot Operating System 2 (ROS 2), which serves as the middleware for robot control in the Physical AI ecosystem.': 'میڈول 1: د روبوٹک نریوس سسٹم کے پہلے باب میں خوش آمدید۔ اس باب میں، ہم آپ کو روبوٹ آپریٹنگ سسٹم 2 (ROS 2) سے متعارف کرائیں گے، جو فزیکل AI ماحول میں روبوٹ کنٹرول کے لیے مڈل ویئر کا کام کرتا ہے۔',
  'ROS 2 (Robot Operating System 2) is not an actual operating system but rather a flexible framework for writing robot software. It\'s a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms and environments.': 'ROS 2 (روبوٹ آپریٹنگ سسٹم 2) اصل میں کوئی آپریٹنگ سسٹم نہیں ہے بلکہ روبوٹ سافٹ ویئر لکھنے کے لیے ایک لچکدار فریم ورک ہے۔ یہ اوزاروں، لائبریریز اور رواجوں کا ایک مجموعہ ہے جو مختلف قسم کے روبوٹ پلیٹ فارمز اور ماحول میں پیچیدہ اور مضبوط روبوٹ کے رویے کو بنانے کے کام کو آسان بنانے کا مقصد رکھتا ہے۔',
  'Distributed computing': 'تقسیم شدہ کمپیوٹنگ',
  'Language independence': 'زبان کی آزادی',
  'Platform independence': 'پلیٹ فارم کی آزادی',
  'Package management': 'پیکیج مینجمنٹ',
  'Real-time capabilities': 'ریل ٹائم صلاحیتیں',
  'In the context of Physical AI and humanoid robotics, ROS 2 serves as the "nervous system" of the robot. It enables:': 'فزیکل AI اور ہیومنوائڈ روبوٹکس کے تناظر میں، ROS 2 روبوٹ کے "نروس سسٹم" کا کام کرتا ہے۔ یہ فعال کرتا ہے:',
  'Communication between different robot components (sensors, actuators, processing units)': 'مختلف روبوٹ اجزاء کے درمیان مواصلت (سینسرز، ایکچو ایٹرز، پروسیسنگ یونٹس)',
  'Integration of AI algorithms with physical robot control': 'AI الگورتھم کو جسمانی روبوٹ کنٹرول کے ساتھ یکجہتی',
  'Simulation-to-reality transfer through consistent interfaces': 'مطابق انٹرفیسز کے ذریعے سیمولیشن سے حقیقت میں منتقلی',
  'Collaboration between multiple robots or between robots and humans': 'متعدد روبوٹس کے درمیان یا روبوٹس اور انسانوں کے درمیان تعاون',
  'The architecture of ROS 2 is built around the concept of nodes, which are individual processes that perform computation. Nodes are organized into packages, which are collections of related functionality.': 'ROS 2 کا معماری نوڈس کے تصور کے گرد تعمیر کیا گیا ہے، جو انفرادی عمل ہیں جو حساب کتاب انجام دیتے ہیں۔ نوڈس کو پیکیجز میں منظم کیا جاتا ہے، جو متعلقہ افعال کا مجموعہ ہیں۔',
  'ROS 2 uses Data Distribution Service (DDS) as its communication layer. DDS is a middleware standard that provides:': 'ROS 2 ڈیٹا ڈسٹری بیوشن سروس (DDS) کو اپنے مواصلاتی لیئر کے طور پر استعمال کرتا ہے۔ DDS ایک مڈل ویئر معیار ہے جو فراہم کرتا ہے:',
  'Publisher/Subscriber model': 'پبلشر/سبسکرائبر ماڈل',
  'Request/Reply model': 'ریکویسٹ/ریپلائی ماڈل',
  'Discovery': 'ڈسکوری',
  'Quality of Service (QoS) settings': 'سروس کے معیار (QoS) کی ترتیبات',
  'For this course, we recommend installing the latest LTS version of ROS 2 (currently Humble Hawksbill for Ubuntu 22.04). If you\'re using a Jetson platform, you\'ll need to follow the ARM64 installation instructions.': 'اس کورس کے لیے، ہم ROS 2 کے تازہ ترین LTS ورژن کی تنصیب کی سفارش کرتے ہیں (فی الحال Ubuntu 22.04 کے لیے ہمبل ہاکسبلڈ)۔ اگر آپ Jetson پلیٹ فارم استعمال کر رہے ہیں، تو آپ کو ARM64 تنصیب کی ہدایات پر عمل کرنا ہوگا۔',
  'Here are some essential ROS 2 commands you\'ll use throughout this module:': 'یہاں کچھ اہم ROS 2 کمانڈز ہیں جن کا آپ اس ماڈیول میں استعمال کریں گے:',
  'Source the ROS 2 environment': 'ROS 2 ماحول کو سورس کریں',
  'List all active nodes': 'تمام فعال نوڈس کی فہرست',
  'List all active topics': 'تمام فعال ٹاپکس کی فہرست',
  'List all active services': 'تمام فعال سروسز کی فہرست',
  'ROS 2 was designed to address several limitations of ROS 1:': 'ROS 2 کو ROS 1 کی کئی حدود کو حل کرنے کے لیے ڈیزائن کیا گیا تھا:',
  'Real-time support': 'ریل ٹائم سپورٹ',
  'Multi-robot systems': 'ملٹی روبوٹ سسٹم',
  'Security': 'سیکورٹی',
  'DDS-based communication': 'DDS-مبنی مواصلات',
  'OS platform support': 'OS پلیٹ فارم سپورٹ',
  'In the next chapter, we\'ll dive deeper into ROS 2 nodes, topics, and services - the fundamental building blocks of ROS 2 communication.': 'اگلے باب میں، ہم ROS 2 نوڈس، ٹاپکس، اور سروسز میں اور گہرائی سے جائیں گے - ROS 2 مواصلات کے بنیادی جزوں میں.',
  'In this chapter, you learned:': 'اس باب میں آپ نے سیکھا:',
  'What ROS 2 is and why it\'s important for Physical AI': 'ROS 2 کیا ہے اور فزیکل AI کے لیے یہ کیوں اہم ہے',
  'The key features and architecture of ROS 2': 'ROS 2 کی کلیدی خصوصیات اور آرکیٹیکچر',
  'How ROS 2 serves as the "nervous system" for humanoid robots': 'کیسے ROS 2 ہیومنوائڈ روبوٹس کے لیے "نروس سسٹم" کا کام کرتا ہے',
  'Basic ROS 2 commands to get started': 'شروع کرنے کے لیے بنیادی ROS 2 کمانڈز',
  'Continue to': 'جاری رکھیں',
  'Chapter 2: ROS 2 Nodes and Topics': 'باب 2: ROS 2 نوڈس اور ٹاپکس',
};

// Backend translation API - using our own backend service
const translateWithBackendAPI = async (text, targetLang) => {
  try {
    // Using our own backend translation endpoint
    const response = await fetch('/api/v1/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        target_lang: targetLang
      })
    });

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status}`);
    }

    const data = await response.json();
    return data.translated_text;
  } catch (error) {
    console.error('Backend Translation API failed:', error);
    // Fallback to our translation map if API fails
    return TRANSLATION_MAP[text] || text;
  }
};

// Alternative: Using bulk translation for multiple texts
const translateBulkWithBackendAPI = async (texts, targetLang) => {
  try {
    const response = await fetch('/api/v1/translate-bulk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        texts: texts,
        target_lang: targetLang
      })
    });

    if (!response.ok) {
      throw new Error(`Bulk translation API error: ${response.status}`);
    }

    const data = await response.json();
    return data.translated_texts;
  } catch (error) {
    console.error('Backend Bulk Translation API failed:', error);
    // Fallback to our translation map if API fails
    return texts.map(text => TRANSLATION_MAP[text] || text);
  }
};

// Choose which API to use
const translateAPI = async (text, targetLang) => {
  try {
    return await translateWithBackendAPI(text, targetLang);
  } catch (error) {
    console.warn('Backend Translation API failed, using translation map:', error);
    // Final fallback to our translation map
    return TRANSLATION_MAP[text] || text;
  }
};

// Translation service class
class TranslationService {
  constructor() {
    this.cache = new Map();
  }

  async translateText(text, targetLang) {
    const cacheKey = `${text}-${targetLang}`;

    // Check if translation is already cached
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    try {
      const translatedText = await translateAPI(text, targetLang);

      // Cache the result
      this.cache.set(cacheKey, translatedText);

      return translatedText;
    } catch (error) {
      console.error('Translation failed:', error);
      throw error;
    }
  }

  // Function to translate content recursively
  async translateContent(content, targetLang) {
    if (targetLang === 'en') {
      // If switching back to English, return original content
      return content;
    }

    if (typeof content === 'string') {
      if (content.trim() === '') return content;
      const translated = await this.translateText(content, targetLang);
      return translated;
    }

    if (Array.isArray(content)) {
      const translatedArray = [];
      for (const item of content) {
        translatedArray.push(await this.translateContent(item, targetLang));
      }
      return translatedArray;
    }

    if (React.isValidElement(content)) {
      const { children, ...props } = content;

      // Don't translate code blocks, links, or other special elements
      if (content.type === 'code' || content.type === 'pre' || content.type === 'a' || content.type === 'img') {
        const translatedChildren = children ? await this.translateContent(children, targetLang) : children;
        return React.cloneElement(content, props, translatedChildren);
      }

      const translatedChildren = children ? await this.translateContent(children, targetLang) : children;
      return React.cloneElement(content, props, translatedChildren);
    }

    return content;
  }
}

export default new TranslationService();